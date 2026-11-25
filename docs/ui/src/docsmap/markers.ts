import type { Point } from "@/geometry";
import type { Destination, MapLayout } from "@/docsmap/layout";

const END_ALIGNED_FROM = 0.8;

/**
 * Where a marker sits on the map, as CSS percentages of the map's size.
 */
export interface Position {
    readonly left: string;
    readonly top: string;
}

/**
 * A destination's marker on the map. `room` is the space between the marker and the map edge
 * that its label extends towards.
 */
export interface Marker {
    readonly destination: Destination;
    readonly index: number;
    readonly position: Position;
    readonly room: string;
    readonly upper: boolean;
    readonly endAligned: boolean;
}

/**
 * Places a marker for each destination at its place in `layout`.
 */
export function markersOf(destinations: readonly Destination[], layout: MapLayout): Marker[] {
    return destinations.map((destination, index) => markerAt({ layout, destination, index }));
}

/**
 * Returns where the planner's start sits on the map.
 */
export function startPosition(layout: MapLayout): Position {
    return positionOf(layout, [layout.start.x, layout.start.y]);
}

function markerAt({ layout, destination, index }: { layout: MapLayout; destination: Destination; index: number }): Marker {
    const place = placeOf(layout, index);
    const endAligned = place[0] > layout.width * END_ALIGNED_FROM;
    const room = endAligned ? place[0] : layout.width - place[0];
    return {
        destination,
        index,
        position: positionOf(layout, place),
        room: percent(room, layout.width),
        upper: place[1] < layout.height / 2,
        endAligned,
    };
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
