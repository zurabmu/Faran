import type { Point } from "@/geometry";
import { dropOnWater } from "@/water";

/**
 * Lets a drop fall at a point in the viewBox coordinates of the SVG that holds `part`.
 */
export function dropAtMarkPoint(part: SVGElement, [x, y]: Point): void {
    const toScreen = part.ownerSVGElement?.getScreenCTM() ?? null;
    if (toScreen === null) return;
    const point = new DOMPoint(x, y).matrixTransform(toScreen);
    dropOnWater({ x: point.x, y: point.y, strength: 0.7 });
}
