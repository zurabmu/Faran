export type Point = readonly [number, number];

export interface Frame {
    readonly point: Point;
    readonly tangent: Point;
}

/**
 * One arc or straight segment of a path. Distances are path lengths in canvas units from the
 * start of the piece.
 */
export interface Piece {
    readonly length: number;
    frameAt(distance: number): Frame;
    rotatedHalfTurn(): Piece;
    reversed(): Piece;
    pathCommand(): string;
}

/**
 * A sequence of pieces that join with matching tangents.
 * A distance past the last piece continues along the last piece.
 */
export interface Stroke {
    readonly length: number;
    frameAt(distance: number): Frame;
    pathData(): string;
}

const DEGREE = Math.PI / 180;
const round = (value: number) => Math.round(value * 100) / 100;
const format = ([x, y]: Point) => `${round(x)} ${round(y)}`;

function arc(center: Point, radius: number, fromDegrees: number, toDegrees: number): Piece {
    const direction = Math.sign(toDegrees - fromDegrees);
    const pointAt = (degrees: number): Point => [
        center[0] + radius * Math.cos(degrees * DEGREE),
        center[1] + radius * Math.sin(degrees * DEGREE),
    ];
    return {
        length: Math.abs(toDegrees - fromDegrees) * DEGREE * radius,
        frameAt(distance) {
            const degrees = fromDegrees + (direction * distance) / radius / DEGREE;
            return {
                point: pointAt(degrees),
                tangent: [-direction * Math.sin(degrees * DEGREE), direction * Math.cos(degrees * DEGREE)],
            };
        },
        rotatedHalfTurn: () => arc([-center[0], -center[1]], radius, fromDegrees + 180, toDegrees + 180),
        reversed: () => arc(center, radius, toDegrees, fromDegrees),
        pathCommand() {
            const isLarge = Math.abs(toDegrees - fromDegrees) > 180 ? 1 : 0;
            const sweep = direction > 0 ? 1 : 0;
            return `A${radius} ${radius} 0 ${isLarge} ${sweep} ${format(pointAt(toDegrees))}`;
        },
    };
}

function line(start: Point, end: Point): Piece {
    const length = Math.hypot(end[0] - start[0], end[1] - start[1]);
    const tangent: Point = [(end[0] - start[0]) / length, (end[1] - start[1]) / length];
    return {
        length,
        frameAt: (distance) => ({ point: [start[0] + tangent[0] * distance, start[1] + tangent[1] * distance], tangent }),
        rotatedHalfTurn: () => line([-start[0], -start[1]], [-end[0], -end[1]]),
        reversed: () => line(end, start),
        pathCommand: () => `L${format(end)}`,
    };
}

/**
 * Factories for path pieces. Angles are in degrees, measured clockwise
 * from the positive x axis in SVG coordinates, and an arc runs from the first angle to the second.
 */
export const piece = { arc, line };

/**
 * Joins pieces into one stroke, without the pieces shorter than a hundredth of a unit.
 */
export function stroke(pieces: readonly Piece[]): Stroke {
    const kept = pieces.filter((candidate) => candidate.length > 0.01);
    const first = kept[0];
    const last = kept.at(-1);
    if (first === undefined || last === undefined) throw new Error(`A stroke needs at least one piece longer than 0.01, got ${pieces.length} pieces`);
    return {
        length: kept.reduce((sum, candidate) => sum + candidate.length, 0),
        frameAt(distance) {
            let rest = Math.max(0, distance);
            for (const candidate of kept) {
                if (rest <= candidate.length || candidate === last) return candidate.frameAt(rest);
                rest -= candidate.length;
            }
            return last.frameAt(rest);
        },
        pathData: () => `M${format(first.frameAt(0).point)}${kept.map((candidate) => candidate.pathCommand()).join("")}`,
    };
}

/**
 * Formats a point for SVG path data, rounded to two decimals.
 */
export const formatPoint = format;
