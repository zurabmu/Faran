const GAUSSIAN_REACH = 2.5;
const RESTING_EDGE = 1;

/**
 * A height field on a regular grid that follows the damped two-dimensional wave equation.
 * Heights are in arbitrary units around a rest level of zero, and positions are in grid cells.
 * The cells at the edge stay at rest.
 */
export class WaveField {
    #current: Float32Array;
    #previous: Float32Array;

    constructor(
        readonly columns: number,
        readonly rows: number,
        private readonly damping: number,
    ) {
        this.#current = new Float32Array(columns * rows);
        this.#previous = new Float32Array(columns * rows);
    }

    /**
     * The heights in row-major order, top row first. The array is replaced on every step.
     */
    get heights(): Float32Array {
        return this.#current;
    }

    /**
     * Raises the surface by `amount` at the given cell, spread over a Gaussian of the given radius.
     */
    disturb({ column, row, radius, amount }: { column: number; row: number; radius: number; amount: number }): void {
        const reach = Math.ceil(radius * GAUSSIAN_REACH);
        const columns = this.#interiorAround(column, reach, this.columns);
        for (const y of this.#interiorAround(row, reach, this.rows)) {
            for (const x of columns) this.#raise(x, y, amount * gaussian({ dx: x - column, dy: y - row, radius }));
        }
    }

    /**
     * Advances the surface by one time step.
     */
    step(): void {
        const next = this.#previous;
        for (let y = RESTING_EDGE; y < this.rows - RESTING_EDGE; y += 1) this.#stepRow(y, next);
        this.#previous = this.#current;
        this.#current = next;
    }

    /**
     * Moves the surface up by `rows` grid rows, or down when `rows` is negative. Rows that move in
     * at the edge are at rest.
     */
    shift(rows: number): void {
        this.#current = shifted(this.#current, { rows, columns: this.columns });
        this.#previous = shifted(this.#previous, { rows, columns: this.columns });
    }

    /**
     * The largest absolute height on the surface.
     */
    peak(): number {
        let largest = 0;
        for (const height of this.#current) largest = Math.max(largest, Math.abs(height));
        return largest;
    }

    #stepRow(y: number, next: Float32Array): void {
        const current = this.#current;
        const { columns, damping } = this;
        // The loop body is inlined, as it runs for every cell twice per animation frame.
        for (let index = y * columns + RESTING_EDGE, end = (y + 1) * columns - RESTING_EDGE; index < end; index += 1) {
            const neighbors = current[index - 1]! + current[index + 1]! + current[index - columns]! + current[index + columns]!;
            next[index] = (neighbors / 2 - next[index]!) * damping;
        }
    }

    #raise(x: number, y: number, amount: number): void {
        const index = y * this.columns + x;
        this.#current[index] = this.#current[index]! + amount;
    }

    #interiorAround(center: number, reach: number, size: number): number[] {
        const first = Math.max(RESTING_EDGE, Math.floor(center - reach));
        const last = Math.min(size - 1 - RESTING_EDGE, Math.ceil(center + reach));
        return Array.from({ length: Math.max(0, last - first + 1) }, (_, offset) => first + offset);
    }
}

function gaussian({ dx, dy, radius }: { dx: number; dy: number; radius: number }): number {
    return Math.exp(-(dx * dx + dy * dy) / (2 * radius * radius));
}

function shifted(heights: Float32Array, { rows, columns }: { rows: number; columns: number }): Float32Array {
    const moved = new Float32Array(heights.length);
    const offset = rows * columns;
    if (offset >= 0) moved.set(heights.subarray(Math.min(offset, heights.length)));
    else moved.set(heights.subarray(0, Math.max(0, heights.length + offset)), Math.min(-offset, heights.length));
    return moved;
}
