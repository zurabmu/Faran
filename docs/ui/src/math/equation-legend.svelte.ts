import { formulaOf, type LegendSymbol, symbolsOf } from "@/math/content";
import { occurrencesOf } from "@/math/occurrences";
import { LegendSelection } from "@/math/selection.svelte";

const HIGHLIGHT_CLASS = "is-highlighted";

/**
 * The legend of an `/// equation` block: its symbols, which one is shown, and the highlight of
 * the shown symbol where it occurs in the formula. Create it while a component initializes,
 * after the formula is typeset.
 */
export class EquationLegend {
    readonly symbols: readonly LegendSymbol[];
    readonly selection = new LegendSelection();
    readonly #occurrences: readonly (readonly Element[])[];

    constructor(private readonly host: HTMLElement) {
        const formula = formulaOf(host);
        this.symbols = symbolsOf(host);
        this.#occurrences = this.symbols.map(({ notation }) => occurrencesOf({ formula, notation }));
        $effect(() => this.#highlight(this.selection.shown));
    }

    /**
     * Clears the selection when the pointer goes down outside the equation.
     */
    clearOutside(event: PointerEvent): void {
        const isOutside = !event.composedPath().includes(this.host);
        if (isOutside) this.selection.clear();
    }

    #highlight(shown: number): void {
        this.#occurrences.forEach((atoms, index) => {
            for (const atom of atoms) atom.classList.toggle(HIGHLIGHT_CLASS, index === shown);
        });
    }
}
