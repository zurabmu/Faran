import { DynamicDrawUsage, Group, InstancedInterleavedBuffer, InterleavedBufferAttribute } from "three";
import { LineMaterial } from "three/addons/lines/LineMaterial.js";
import { LineSegments2 } from "three/addons/lines/LineSegments2.js";
import { LineSegmentsGeometry } from "three/addons/lines/LineSegmentsGeometry.js";
import type { LineStyle, Point, Rendering } from "@/animation";
import { type Dashes, dashesFor } from "@/style";
import type { CameraBox } from "@/view";
import type { Layer, Viewport } from "@/scene/layer";
import { paint } from "@/scene/paint";
import { markWritten } from "@/scene/upload";

const POINT_FLOATS = 3;
const DISTANCE_FLOATS = 1;
const SEGMENT_POSITION_FLOATS = 2 * POINT_FLOATS;
const SEGMENT_DISTANCE_FLOATS = 2 * DISTANCE_FLOATS;
const INSTANCES_PER_SEGMENT = 1;
const NO_STRIPS: readonly (readonly Point[])[] = [];

/**
 * Shows a lines rendering as one set of line segments, dashed or not, in a single draw call.
 * Dashes start anew at the first point of each strip.
 */
export class LinesLayer implements Layer {
    readonly object = new Group();
    #segments = new Segments(1);
    #strips = NO_STRIPS;
    readonly #line = new LineSegments2(this.#segments.geometry, new LineMaterial({ worldUnits: false, transparent: true, depthTest: false }));

    constructor() {
        this.#line.frustumCulled = false;
        this.object.add(this.#line);
    }

    show(rendering: Rendering, viewport: Viewport): boolean {
        if (rendering.kind !== "lines") return false;
        this.#applyStyle(rendering.style, viewport);
        const stripsChanged = rendering.strips !== this.#strips;
        if (stripsChanged) this.#upload(rendering.strips);
        return true;
    }

    dispose(): void {
        this.#segments.geometry.dispose();
        this.#line.material.dispose();
    }

    #applyStyle({ color, width, pattern }: LineStyle, viewport: Viewport): void {
        const material = this.#line.material;
        material.linewidth = width;
        material.resolution.set(viewport.width, viewport.height);
        this.#applyDashes(dashesFor(pattern, width), viewport.box);
        paint(material, color);
    }

    #applyDashes(dashes: Dashes, { scale }: CameraBox): void {
        const material = this.#line.material;
        const isSolid = dashes.length === 0;
        material.dashed = !isSolid;
        if (isSolid) return;
        const [dash, gap] = dashes;
        material.dashSize = dash / scale;
        material.gapSize = gap / scale;
    }

    #upload(strips: readonly (readonly Point[])[]): void {
        this.#strips = strips;
        const count = segmentCount(strips);
        this.#reserve(count);
        this.#segments.write(strips, count);
    }

    #reserve(count: number): void {
        const capacity = this.#segments.capacity;
        const exceedsCapacity = count > capacity;
        if (exceedsCapacity) this.#replaceSegments(Math.max(count, 2 * capacity));
    }

    #replaceSegments(capacity: number): void {
        this.#segments.geometry.dispose();
        this.#segments = new Segments(capacity);
        this.#line.geometry = this.#segments.geometry;
    }
}

class Segments {
    readonly geometry = new LineSegmentsGeometry();
    readonly #positions: InstancedInterleavedBuffer;
    readonly #distances: InstancedInterleavedBuffer;

    constructor(readonly capacity: number) {
        this.#positions = segmentBuffer({ capacity, floatsPerSegment: SEGMENT_POSITION_FLOATS });
        this.#distances = segmentBuffer({ capacity, floatsPerSegment: SEGMENT_DISTANCE_FLOATS });
        this.#placeSegmentsBy(this.#positions);
        this.#placeDashesBy(this.#distances);
        this.geometry.instanceCount = 0;
    }

    write(strips: readonly (readonly Point[])[], count: number): void {
        let firstIndex = 0;
        for (const strip of strips) firstIndex = this.#writeStrip(strip, { firstIndex });
        markWritten(this.#positions, count * SEGMENT_POSITION_FLOATS);
        markWritten(this.#distances, count * SEGMENT_DISTANCE_FLOATS);
        this.geometry.instanceCount = count;
    }

    #writeStrip(strip: readonly Point[], { firstIndex }: { firstIndex: number }): number {
        let index = firstIndex;
        let distance = 0;
        for (const [start, end] of consecutivePairs(strip)) {
            this.#writeSegment({ index, start, end, distance });
            distance += lengthBetween(start, end);
            index += 1;
        }
        return index;
    }

    #placeSegmentsBy(positions: InstancedInterleavedBuffer): void {
        this.#bindEndpointAttributes(positions, { start: "instanceStart", end: "instanceEnd", floatsPerEndpoint: POINT_FLOATS });
    }

    #placeDashesBy(distances: InstancedInterleavedBuffer): void {
        this.#bindEndpointAttributes(distances, { start: "instanceDistanceStart", end: "instanceDistanceEnd", floatsPerEndpoint: DISTANCE_FLOATS });
    }

    #bindEndpointAttributes(
        buffer: InstancedInterleavedBuffer,
        { start, end, floatsPerEndpoint }: { start: string; end: string; floatsPerEndpoint: number },
    ): void {
        this.geometry.setAttribute(start, new InterleavedBufferAttribute(buffer, floatsPerEndpoint, 0));
        this.geometry.setAttribute(end, new InterleavedBufferAttribute(buffer, floatsPerEndpoint, floatsPerEndpoint));
    }

    #writeSegment({ index, start, end, distance }: { index: number; start: Point; end: Point; distance: number }): void {
        const positions = this.#positions.array as Float32Array;
        const distances = this.#distances.array as Float32Array;
        const positionOffset = index * SEGMENT_POSITION_FLOATS;
        positions.set(start, positionOffset);
        positions.set(end, positionOffset + POINT_FLOATS);
        const distanceOffset = index * SEGMENT_DISTANCE_FLOATS;
        distances[distanceOffset] = distance;
        distances[distanceOffset + DISTANCE_FLOATS] = distance + lengthBetween(start, end);
    }
}

function segmentBuffer({ capacity, floatsPerSegment }: { capacity: number; floatsPerSegment: number }): InstancedInterleavedBuffer {
    const floats = new Float32Array(capacity * floatsPerSegment);
    return new InstancedInterleavedBuffer(floats, floatsPerSegment, INSTANCES_PER_SEGMENT).setUsage(DynamicDrawUsage);
}

function* consecutivePairs(strip: readonly Point[]): Generator<[Point, Point]> {
    for (let index = 1; index < strip.length; index += 1) yield [strip[index - 1]!, strip[index]!];
}

function lengthBetween([startX, startY]: Point, [endX, endY]: Point): number {
    return Math.hypot(endX - startX, endY - startY);
}

function segmentCount(strips: readonly (readonly Point[])[]): number {
    return strips.reduce((count, strip) => count + Math.max(0, strip.length - 1), 0);
}
