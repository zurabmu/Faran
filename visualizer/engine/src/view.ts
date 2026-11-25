import type { Point, Rendering } from "@engine/animation";

const SMALLEST_SCENE_EXTENT = 1e-9;

/**
 * The part of the scene to show, in scene units.
 */
export interface Bounds {
    readonly left: number;
    readonly bottom: number;
    readonly right: number;
    readonly top: number;
}

/**
 * The area of the scene that a canvas shows, in scene units with y pointing up, and how many
 * CSS pixels one scene unit takes.
 */
export interface CameraBox extends Bounds {
    readonly scale: number;
}

/**
 * Returns the smallest bounds that hold every point of the renderings.
 * Fails when the renderings hold no points.
 */
export function boundsOf(renderings: readonly Rendering[]): Bounds {
    let [left, bottom, right, top] = [Infinity, Infinity, -Infinity, -Infinity];
    const include = ([x, y]: Point) => {
        left = Math.min(left, x);
        right = Math.max(right, x);
        bottom = Math.min(bottom, y);
        top = Math.max(top, y);
    };
    for (const rendering of renderings) pointsOf(rendering).forEach(include);
    const holdsNoPoints = left > right;
    if (holdsNoPoints) throw new Error("Expected the renderings to hold at least one point to fit the view to.");
    return { left, right, bottom, top };
}

function pointsOf(rendering: Rendering): readonly Point[] {
    return rendering.kind === "lines" ? rendering.strips.flat() : rendering.positions;
}

/**
 * Returns the area a canvas of `width` by `height` CSS pixels shows so that all of `bounds`
 * appears as large as fits, centered, with `padding` pixels left free on every side.
 */
export function cameraBox({ bounds, width, height, padding }: { bounds: Bounds; width: number; height: number; padding: number }): CameraBox {
    const sceneWidth = Math.max(bounds.right - bounds.left, SMALLEST_SCENE_EXTENT);
    const sceneHeight = Math.max(bounds.top - bounds.bottom, SMALLEST_SCENE_EXTENT);
    const scale = Math.min((width - 2 * padding) / sceneWidth, (height - 2 * padding) / sceneHeight);
    const centerX = (bounds.left + bounds.right) / 2;
    const centerY = (bounds.bottom + bounds.top) / 2;
    const halfWidth = width / 2 / scale;
    const halfHeight = height / 2 / scale;
    return {
        scale,
        left: centerX - halfWidth,
        right: centerX + halfWidth,
        bottom: centerY - halfHeight,
        top: centerY + halfHeight,
    };
}
