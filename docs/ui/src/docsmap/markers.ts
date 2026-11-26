import type { Point } from "@/geometry";
import type { Destination, MapLayout } from "@/docsmap/layout";

const END_ALIGNED_FROM = 0.8;
const LABEL_GAP = 0.6;

/**
 * Where a marker sits on the map, as CSS percentages of the map's size.
 */
export interface Position {
    readonly left: string;
    readonly top: string;
}

/** `room` and `indent` are percentages of the map's width. */
export interface Placement {
    readonly position: Position;
    readonly room: string;
    readonly indent: string;
    readonly upper: boolean;
    readonly endAligned: boolean;
}

export interface Marker extends Placement {
    readonly destination: Destination;
    readonly index: number;
}

export interface Labeling {
    place(layout: MapLayout, point: Point): Placement;
    placeHome(layout: MapLayout): Placement;
}

/** Labels below the upper places and above the lower ones. */
export const labelsAround: Labeling = {
    place(layout, point) {
        const endAligned = point[0] > layout.width * END_ALIGNED_FROM;
        const room = endAligned ? point[0] : layout.width - point[0];
        return { position: positionOf(layout, point), room: percent(room, layout.width), indent: "0%", upper: point[1] < layout.height / 2, endAligned };
    },
    placeHome(layout) {
        return { position: positionOf(layout, [layout.start.x, layout.start.y]), room: "100%", indent: "0%", upper: true, endAligned: false };
    },
};

/** Labels in one column right of the places. */
export const labelsBeside: Labeling = {
    place(layout, point) {
        return besidePlacement(layout, point);
    },
    placeHome(layout) {
        return besidePlacement(layout, [layout.start.x, layout.start.y]);
    },
};

/**
 * Places a marker for each destination at its place in `layout`.
 */
export function markersOf({ destinations, layout, labeling }: { destinations: readonly Destination[]; layout: MapLayout; labeling: Labeling }): Marker[] {
    return destinations.map((destination, index) => ({ destination, index, ...labeling.place(layout, placeOf(layout, index)) }));
}

function besidePlacement(layout: MapLayout, point: Point): Placement {
    const labelX = labelColumnOf(layout);
    return {
        position: positionOf(layout, point),
        room: percent(layout.width - point[0], layout.width),
        indent: percent(labelX - point[0], layout.width),
        upper: true,
        endAligned: false,
    };
}

function labelColumnOf(layout: MapLayout): number {
    const rightEdges = [...layout.places.map(([x]) => x), ...layout.obstacles.map(({ center, radius }) => center[0] + radius)];
    return Math.max(...rightEdges) + LABEL_GAP;
}

function placeOf(layout: MapLayout, index: number): Point {
    const place = layout.places[index];
    if (place === undefined) throw new Error(`Expected the map layout to have a place for destination ${index + 1}, but it has ${layout.places.length} places.`);
    return place;
}

function positionOf(layout: MapLayout, [x, y]: Point): Position {
    return { left: percent(x, layout.width), top: percent(y, layout.height) };
}

function percent(value: number, total: number): string {
    return `${(value / total) * 100}%`;
}
