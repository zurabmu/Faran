import type { Dots, Frame, Lines, Point, Rendering } from "@engine";

/**
 * Returns `start` with each point moved `fraction` of the way to its point in `end`. Both frames
 * must have the same renderings with the same number of points.
 */
export function interpolateFrames(start: Frame, end: Frame, fraction: number): Frame {
    const renderings = pairs("renderings", start.renderings, end.renderings).map(([from, to]) => interpolateRendering(from, to, fraction));
    return { ...start, renderings };
}

function interpolateRendering(start: Rendering, end: Rendering, fraction: number): Rendering {
    if (start.kind === "dots") return interpolateDots(start, matching(start, end), fraction);
    return interpolateLines(start, matching(start, end), fraction);
}

function interpolateDots(start: Dots, end: Dots, fraction: number): Dots {
    return { ...start, positions: interpolatePoints(start.positions, end.positions, fraction) };
}

function interpolateLines(start: Lines, end: Lines, fraction: number): Lines {
    const strips = pairs(`strips of "${start.name}"`, start.strips, end.strips).map(([from, to]) => interpolatePoints(from, to, fraction));
    return { ...start, strips };
}

function interpolatePoints(start: readonly Point[], end: readonly Point[], fraction: number): Point[] {
    return pairs("points", start, end).map(([from, to]) => interpolatePoint(from, to, fraction));
}

function interpolatePoint([x, y]: Point, [endX, endY]: Point, fraction: number): Point {
    return [x + (endX - x) * fraction, y + (endY - y) * fraction];
}

function matching<Kind extends Rendering>(start: Kind, end: Rendering): Kind {
    const isSameRendering = end.kind === start.kind && end.name === start.name;
    if (!isSameRendering) throw new Error(`Expected the end of rendering "${start.name}" to be ${start.kind} with the same name, but it is ${end.kind} "${end.name}".`);
    return end as Kind;
}

function pairs<Item>(items: string, start: readonly Item[], end: readonly Item[]): [Item, Item][] {
    if (start.length !== end.length) throw new Error(`Expected as many ${items} at the end as at the start, ${start.length}, but there are ${end.length}.`);
    return start.map((item, index) => [item, end[index] as Item]);
}
