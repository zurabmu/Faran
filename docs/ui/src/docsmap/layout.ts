import type { Point } from "@/geometry";

/**
 * A circular obstacle in field units.
 */
export interface Circle {
    readonly center: Point;
    readonly radius: number;
}

/**
 * Where the planner starts: a position in field units and a heading in radians.
 */
export interface Pose {
    readonly x: number;
    readonly y: number;
    readonly heading: number;
}

/**
 * A section of the documentation that the map links to.
 */
export interface Destination {
    readonly title: string;
    readonly href: string;
    readonly description: string;
}

/**
 * A docs map in field units, with y pointing down.
 */
export interface MapLayout {
    readonly width: number;
    readonly height: number;
    readonly places: readonly Point[];
    readonly obstacles: readonly Circle[];
    readonly start: Pose;
}

const WIDE = {
    width: 12,
    height: 4.4,
    firstX: 3.4,
    lastX: 11,
    upperY: 0.9,
    lowerY: 3.5,
    obstacleAfterUpperY: 2.45,
    obstacleAfterLowerY: 1.95,
};
const WIDE_START: Pose = { x: 0.7, y: WIDE.height / 2, heading: 0 };
const WIDE_OBSTACLE_AHEAD_OF_START: Circle = { center: [2.1, WIDE.height / 2], radius: 0.5 };

const TALL = {
    width: 6,
    firstY: 2.9,
    spacing: 1.8,
    leftX: 0.6,
    rightX: 2,
    bottomMargin: 1.4,
    obstacleShift: 0.15,
};
const TALL_START: Pose = { x: (TALL.leftX + TALL.rightX) / 2, y: 0.6, heading: Math.PI / 2 };
const TALL_OBSTACLE_AHEAD_OF_START: Circle = { center: [TALL_START.x, 1.6], radius: 0.45 };

const OBSTACLE_BETWEEN_RADIUS = 0.42;

/**
 * Places the destinations from left to right, alternating between an upper and a lower row,
 * with one obstacle between each pair of neighbors.
 */
export function wideMapLayout(count: number): MapLayout {
    const places = Array.from({ length: count }, (_, index): Point => [wideX(index, count), isFirstOfPair(index) ? WIDE.upperY : WIDE.lowerY]);
    const obstacles = neighbors(places).map(([left, right], index): Circle => ({
        center: [(left[0] + right[0]) / 2, isFirstOfPair(index) ? WIDE.obstacleAfterUpperY : WIDE.obstacleAfterLowerY],
        radius: OBSTACLE_BETWEEN_RADIUS,
    }));
    return { width: WIDE.width, height: WIDE.height, places, obstacles: [WIDE_OBSTACLE_AHEAD_OF_START, ...obstacles], start: WIDE_START };
}

/** Like `wideMapLayout`, but top to bottom in two columns. */
export function tallMapLayout(count: number): MapLayout {
    const places = Array.from({ length: count }, (_, index): Point => [isFirstOfPair(index) ? TALL.leftX : TALL.rightX, TALL.firstY + TALL.spacing * index]);
    const obstacles = neighbors(places).map(([upper, lower], index): Circle => ({
        center: [(upper[0] + lower[0]) / 2 + (isFirstOfPair(index) ? TALL.obstacleShift : -TALL.obstacleShift), (upper[1] + lower[1]) / 2],
        radius: OBSTACLE_BETWEEN_RADIUS,
    }));
    const height = TALL.firstY + TALL.spacing * Math.max(0, count - 1) + TALL.bottomMargin;
    return { width: TALL.width, height, places, obstacles: [TALL_OBSTACLE_AHEAD_OF_START, ...obstacles], start: TALL_START };
}

function wideX(index: number, count: number): number {
    const isAlone = count === 1;
    if (isAlone) return (WIDE.firstX + WIDE.lastX) / 2;
    return WIDE.firstX + ((WIDE.lastX - WIDE.firstX) * index) / (count - 1);
}

function neighbors(places: readonly Point[]): [Point, Point][] {
    return places.slice(1).map((next, index) => [places[index] as Point, next]);
}

function isFirstOfPair(index: number): boolean {
    return index % 2 === 0;
}
