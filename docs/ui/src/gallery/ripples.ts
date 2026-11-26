import { dropOnWater } from "@/water";

const DROP_STRENGTH = 3;

/**
 * Drops at the center of each column. `grid` must use CSS grid layout.
 */
export function dropOnColumnsOf(grid: Element): void {
    const { left, top, height } = grid.getBoundingClientRect();
    const middle = top + height / 2;
    for (const center of columnCentersOf(grid)) {
        dropOnWater({ x: left + center, y: middle, strength: DROP_STRENGTH });
    }
}

function columnCentersOf(grid: Element): number[] {
    const style = getComputedStyle(grid);
    const widths = style.gridTemplateColumns.split(" ").map(Number.parseFloat);
    const gap = Number.parseFloat(style.columnGap);
    const centers: number[] = [];
    let start = 0;
    for (const width of widths) {
        centers.push(start + width / 2);
        start += width + gap;
    }
    return centers;
}
