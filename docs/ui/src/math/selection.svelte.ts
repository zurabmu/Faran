const NO_SYMBOL = -1;

/**
 * Tracks which symbol of a legend is shown: the hovered one, or else the selected one.
 * `shown` is -1 when no symbol is shown.
 */
export class LegendSelection {
    #hovered = $state(NO_SYMBOL);
    #selected = $state(NO_SYMBOL);

    get shown(): number {
        const isHovering = this.#hovered !== NO_SYMBOL;
        return isHovering ? this.#hovered : this.#selected;
    }

    get isEmpty(): boolean {
        return this.shown === NO_SYMBOL;
    }

    hover(index: number): void {
        this.#hovered = index;
    }

    leave(): void {
        this.#hovered = NO_SYMBOL;
    }

    select(index: number): void {
        this.#selected = index;
    }

    clear(): void {
        this.#hovered = NO_SYMBOL;
        this.#selected = NO_SYMBOL;
    }
}
