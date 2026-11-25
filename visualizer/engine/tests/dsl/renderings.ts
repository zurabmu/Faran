import type { Color, LinePattern, Point, Rendering } from "@engine";

const WHITE: Color = [255, 255, 255, 255];

/**
 * A dots rendering with a dot at each of `positions`. Style values the test does not care about
 * get defaults.
 */
export function dots(positions: readonly Point[], { size = 4, color = WHITE }: { size?: number; color?: Color } = {}): Rendering {
    return { kind: "dots", name: "dots", positions, style: { color, size } };
}

/**
 * A lines rendering that connects the points of each strip. Style values the test does not care
 * about get defaults.
 */
export function lines(
    strips: readonly (readonly Point[])[],
    { pattern = "solid", width = 2, color = WHITE }: { pattern?: LinePattern; width?: number; color?: Color } = {},
): Rendering {
    return { kind: "lines", name: "lines", strips, style: { color, width, pattern } };
}

/**
 * The corners of a square with its lower left corner at the origin, counterclockwise.
 */
export function square({ side = 1 }: { side?: number } = {}): Point[] {
    return [
        [0, 0],
        [side, 0],
        [side, side],
        [0, side],
    ];
}
