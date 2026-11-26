import type { ViewportGrid, ViewportPoint } from "@/water/grid";

const SPACING = 2;
const STRENGTH = 0.0048;
const LIMIT = 0.27;
const RADIUS = 1.4;

/**
 * Disturbs the water along the path of a mouse or pen pointer, more strongly the faster it
 * moves.
 */
export class PointerTrail {
    #last: ViewportPoint | undefined;

    constructor(private readonly grid: ViewportGrid) {}

    /**
     * Disturbs the water from the last point to `point`, scaled by `strength`. Returns whether it
     * disturbed it.
     */
    moveTo(point: ViewportPoint, strength: number): boolean {
        const previous = this.#last;
        this.#last = point;
        if (previous === undefined) return false;
        this.#disturbAlong(previous, point, strength);
        return true;
    }

    /**
     * Forgets the last point, so that the next move starts a new trail.
     */
    lift(): void {
        this.#last = undefined;
    }

    #disturbAlong(start: ViewportPoint, end: ViewportPoint, strength: number): void {
        const distance = this.grid.cellsBetween(start, end);
        const amount = Math.min(LIMIT, distance * STRENGTH) * strength;
        const count = Math.max(1, Math.round(distance / SPACING));
        for (let index = 1; index <= count; index += 1) {
            this.grid.disturbAt(between(start, end, index / count), { radius: RADIUS, amount: amount / count });
        }
    }
}

function between(start: ViewportPoint, end: ViewportPoint, share: number): ViewportPoint {
    return { x: start.x + (end.x - start.x) * share, y: start.y + (end.y - start.y) * share };
}
