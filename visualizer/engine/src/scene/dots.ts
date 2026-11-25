import { type CircleGeometry, DynamicDrawUsage, Group, InstancedMesh, Matrix4, MeshBasicMaterial } from "three";
import type { Point, Rendering } from "@engine/animation";
import type { Layer, Viewport } from "@engine/scene/layer";
import { paint } from "@engine/scene/paint";
import { markWritten } from "@engine/scene/upload";

const MATRIX_FLOATS = 16;
const NO_POSITIONS: readonly Point[] = [];

/**
 * Shows a dots rendering as instances of a shared circle, in a single draw call.
 */
export class DotsLayer implements Layer {
    readonly object = new Group();
    readonly #material = new MeshBasicMaterial({ transparent: true, depthTest: false });
    readonly #placement = new Matrix4();
    #mesh: InstancedMesh;
    #positions = NO_POSITIONS;
    #radius = 0;

    /**
     * The circle has a radius of one scene unit and is not disposed with the layer.
     */
    constructor(private readonly circle: CircleGeometry) {
        this.#mesh = this.#addMesh(1);
    }

    show(rendering: Rendering, { box }: Viewport): boolean {
        if (rendering.kind !== "dots") return false;
        paint(this.#material, rendering.style.color);
        const radius = rendering.style.size / 2 / box.scale;
        const placementChanged = rendering.positions !== this.#positions || radius !== this.#radius;
        if (placementChanged) this.#place(rendering.positions, radius);
        return true;
    }

    dispose(): void {
        this.#mesh.dispose();
        this.#material.dispose();
    }

    #place(positions: readonly Point[], radius: number): void {
        this.#positions = positions;
        this.#radius = radius;
        this.#reserve(positions.length);
        positions.forEach((position, index) => this.#mesh.setMatrixAt(index, this.#circleAt(position, radius)));
        this.#mesh.count = positions.length;
        markWritten(this.#mesh.instanceMatrix, positions.length * MATRIX_FLOATS);
    }

    #circleAt([x, y]: Point, radius: number): Matrix4 {
        return this.#placement.makeScale(radius, radius, 1).setPosition(x, y, 0);
    }

    #reserve(count: number): void {
        const capacity = this.#mesh.instanceMatrix.count;
        const exceedsCapacity = count > capacity;
        if (exceedsCapacity) this.#replaceMesh(Math.max(count, 2 * capacity));
    }

    #replaceMesh(capacity: number): void {
        this.object.remove(this.#mesh);
        this.#mesh.dispose();
        this.#mesh = this.#addMesh(capacity);
    }

    #addMesh(capacity: number): InstancedMesh {
        const mesh = new InstancedMesh(this.circle, this.#material, capacity);
        mesh.instanceMatrix.setUsage(DynamicDrawUsage);
        mesh.count = 0;
        mesh.frustumCulled = false;
        this.object.add(mesh);
        return mesh;
    }
}
