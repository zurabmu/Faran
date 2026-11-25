import { type Frame, formatPoint, piece, type Point, type Stroke, stroke } from "@/geometry";
import { brand } from "@/shared/brand";

export interface Body {
    readonly outline: string;
    readonly centerline: string;
    readonly length: number;
    readonly end: Point;
    readonly color: string;
}

/**
 * The parts of the Faran mark, in a viewBox centered on the origin.
 */
export interface MarkDrawing {
    readonly viewBox: string;
    readonly bodies: readonly Body[];
}

const RADIUS = 68;
const WIDTH = 8;
const STEM_X = -7;
const TURN_RADIUS = 23;
const ARM_Y = 9;
const TURN_START_Y = ARM_Y - TURN_RADIUS;
const LOWER_CENTER: readonly [number, number] = [-(STEM_X + RADIUS), 90];
const CURL_RADIUS = LOWER_CENTER[1] - ARM_Y;
const CURL_DEGREES = 42;
const HAIRLINE = 1.2;
const TRAJECTORY_TAPER = 48;
const ARM_TAPER = 46;

interface TaperedStroke {
    readonly stroke: Stroke;
    readonly startTaper: number;
    readonly endTaper: number;
    readonly color: string;
}

const ease = (x: number) => {
    const clamped = Math.min(1, Math.max(0, x));
    return clamped * clamped * (3 - 2 * clamped);
};

interface Edges {
    readonly left: Point;
    readonly right: Point;
}

function outlineOf(tapered: TaperedStroke): string {
    const edges = sampleDistances(tapered.stroke.length).map((distance) => edgesAt(tapered, distance));
    const leftEdge = edges.map(({ left }) => left);
    const rightEdgeBackwards = edges.map(({ right }) => right).reverse();
    return closedPathThrough([...leftEdge, ...rightEdgeBackwards]);
}

function sampleDistances(length: number): number[] {
    const intervals = Math.ceil(length);
    return Array.from({ length: intervals + 1 }, (_, index) => (length * index) / intervals);
}

function edgesAt(tapered: TaperedStroke, distance: number): Edges {
    const frame = tapered.stroke.frameAt(distance);
    const halfWidth = widthAt(tapered, distance) / 2;
    return { left: offsetSideways(frame, halfWidth), right: offsetSideways(frame, -halfWidth) };
}

function widthAt({ stroke: path, startTaper, endTaper }: TaperedStroke, distance: number): number {
    const widthFromStart = taperedWidth(distance / startTaper);
    const widthFromEnd = taperedWidth((path.length - distance) / endTaper);
    return Math.min(widthFromStart, widthFromEnd);
}

function taperedWidth(progress: number): number {
    return HAIRLINE + (WIDTH - HAIRLINE) * ease(progress);
}

function offsetSideways({ point, tangent }: Frame, offset: number): Point {
    const [normalX, normalY] = leftNormalOf(tangent);
    return [point[0] + normalX * offset, point[1] + normalY * offset];
}

function leftNormalOf([x, y]: Point): Point {
    return [y, -x];
}

function closedPathThrough(points: readonly Point[]): string {
    return `M${points.map(formatPoint).join("L")}Z`;
}

export function markDrawing(): MarkDrawing {
    const upperPieces = [
        piece.arc([STEM_X + RADIUS, -90], RADIUS, 320, 180),
        piece.line([STEM_X, -90], [STEM_X, TURN_START_Y]),
        piece.arc([STEM_X - TURN_RADIUS, TURN_START_Y], TURN_RADIUS, 0, 90),
        piece.line([STEM_X - TURN_RADIUS, ARM_Y], [LOWER_CENTER[0], ARM_Y]),
        piece.arc(LOWER_CENTER, CURL_RADIUS, 270, 270 - CURL_DEGREES),
    ];
    const upper = stroke(upperPieces);
    const lower = stroke(upperPieces.map((part) => part.rotatedHalfTurn()).reverse().map((part) => part.reversed()));
    const strokes: TaperedStroke[] = [
        { stroke: upper, startTaper: TRAJECTORY_TAPER, endTaper: ARM_TAPER, color: brand.taken },
        { stroke: lower, startTaper: ARM_TAPER, endTaper: TRAJECTORY_TAPER, color: brand.plan },
    ];
    return {
        viewBox: "-164 -164 328 328",
        bodies: strokes.map((tapered) => ({
            outline: outlineOf(tapered),
            centerline: tapered.stroke.pathData(),
            length: Math.round(tapered.stroke.length),
            end: tapered.stroke.frameAt(tapered.stroke.length).point,
            color: tapered.color,
        })),
    };
}
