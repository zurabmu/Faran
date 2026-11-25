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

const WIDTH = 12;
const HEIGHT = 4.4;
const FIRST_X = 3.4;
const LAST_X = 11;
const UPPER_Y = 0.9;
const LOWER_Y = 3.5;
const START: Pose = { x: 0.7, y: HEIGHT / 2, heading: 0 };
const OBSTACLE_AHEAD_OF_START: Circle = { center: [2.1, HEIGHT / 2], radius: 0.5 };
const OBSTACLE_BETWEEN_RADIUS = 0.42;
const OBSTACLE_AFTER_UPPER_Y = 2.45;
const OBSTACLE_AFTER_LOWER_Y = 1.95;

/**
 * Places the destinations from left to right, alternating between an upper and a lower row,
 * with one obstacle between each pair of neighbors.
 */
export function mapLayout(count: number): MapLayout {
    const places = placesInRows(count);
    return {
        width: WIDTH,
        height: HEIGHT,
        places,
        obstacles: [OBSTACLE_AHEAD_OF_START, ...obstaclesBetween(places)],
        start: START,
    };
}

function placesInRows(count: number): Point[] {
    return Array.from({ length: count }, (_, index) => [placeX(index, count), isInUpperRow(index) ? UPPER_Y : LOWER_Y]);
}

function placeX(index: number, count: number): number {
    const isAlone = count === 1;
    if (isAlone) return (FIRST_X + LAST_X) / 2;
    return FIRST_X + ((LAST_X - FIRST_X) * index) / (count - 1);
}

function obstaclesBetween(places: readonly Point[]): Circle[] {
    return neighbors(places).map(([left, right], index) => ({
        center: [(left[0] + right[0]) / 2, isInUpperRow(index) ? OBSTACLE_AFTER_UPPER_Y : OBSTACLE_AFTER_LOWER_Y],
        radius: OBSTACLE_BETWEEN_RADIUS,
    }));
}

function neighbors(places: readonly Point[]): [Point, Point][] {
    return places.slice(1).map((right, index) => [places[index] as Point, right]);
}

function isInUpperRow(index: number): boolean {
    return index % 2 === 0;
}
