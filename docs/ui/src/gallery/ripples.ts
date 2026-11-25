import { dropOnWater } from "@/water";

const DROP_STRENGTH = 1.5;

/**
 * Lets one drop fall on the water at the left edge of `element` and one at its right edge, both
 * at its vertical middle.
 */
export function dropBeside(element: Element): void {
    const { left, right, top, height } = element.getBoundingClientRect();
    const middle = top + height / 2;
    dropOnWater({ x: left, y: middle, strength: DROP_STRENGTH });
    dropOnWater({ x: right, y: middle, strength: DROP_STRENGTH });
}
