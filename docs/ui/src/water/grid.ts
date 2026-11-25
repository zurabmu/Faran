import { WaveField } from "@/water/field";

const CELL_SIZE = 5;
const MARGIN_CELLS = 2;
const DAMPING = 0.978;

/**
 * A point of the viewport, in CSS pixels.
 */
export interface ViewportPoint {
    readonly x: number;
    readonly y: number;
}

/**
 * The wave field under the viewport. Its rows stay aligned with the page while the page
 * scrolls, so that waves move with the content.
 */
export class ViewportGrid {
    field: WaveField = fieldForViewport();
    #top = alignedTop();

    /**
     * The vertical offset in CSS pixels that keeps the canvas aligned with the field's rows.
     */
    get canvasOffset(): number {
        return this.#top - window.scrollY;
    }

    /**
     * Replaces the field with a flat one of the viewport's size.
     */
    resize(): void {
        this.field = fieldForViewport();
        this.#top = alignedTop();
    }

    /**
     * Moves the field by the rows the page scrolled since the last call.
     */
    followScroll(): void {
        const top = alignedTop();
        this.field.shift((top - this.#top) / CELL_SIZE);
        this.#top = top;
    }

    /**
     * Disturbs the field at a point of the viewport. `radius` is in grid cells.
     */
    disturbAt({ x, y }: ViewportPoint, { radius, amount }: { radius: number; amount: number }): void {
        this.field.disturb({ column: x / CELL_SIZE + 1, row: (y + window.scrollY - this.#top) / CELL_SIZE + 1, radius, amount });
    }

    /**
     * The distance between two points of the viewport, in grid cells.
     */
    cellsBetween(start: ViewportPoint, end: ViewportPoint): number {
        return Math.hypot(end.x - start.x, end.y - start.y) / CELL_SIZE;
    }
}

function fieldForViewport(): WaveField {
    return new WaveField(Math.ceil(window.innerWidth / CELL_SIZE) + MARGIN_CELLS, Math.ceil(window.innerHeight / CELL_SIZE) + MARGIN_CELLS, DAMPING);
}

function alignedTop(): number {
    return Math.floor(window.scrollY / CELL_SIZE) * CELL_SIZE;
}
