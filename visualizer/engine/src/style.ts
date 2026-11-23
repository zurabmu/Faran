import type { Color, LinePattern } from "@/animation";

/**
 * The dash and gap lengths of a line, in screen points. A solid line has none.
 */
export type Dashes = [] | [dash: number, gap: number];

/**
 * Returns the CSS color for an RGBA color with channels from 0 to 255.
 */
export function cssColor([red, green, blue, alpha]: Color): string {
    return `rgba(${red}, ${green}, ${blue}, ${Math.round((alpha / 255) * 1000) / 1000})`;
}

/**
 * Returns the dashes of a line of the given width.
 */
export function dashesFor(pattern: LinePattern, width: number): Dashes {
    if (pattern === "dashed") return [width * 3.5, width * 2.5];
    if (pattern === "dotted") return [width, width * 2.5];
    return [];
}
