import { SvelteMap } from "svelte/reactivity";
import type { ChoiceOption } from "@/shared/choice";
import type { Variant } from "@/variants/variants";

const chosen = new SvelteMap<string, string>();

/**
 * The variant shown by every `<faran-variants>` element with the same label on the page. It is
 * the first variant until the reader chooses one.
 */
export class VariantChoice {
    readonly options: readonly ChoiceOption<string>[];
    readonly #first: Variant;

    constructor(
        private readonly label: string,
        private readonly variants: readonly Variant[],
    ) {
        const [first] = variants;
        if (first === undefined) throw new Error(`Expected the variants "${label}" to have at least one variant, but they have none.`);
        this.#first = first;
        this.options = variants.map(({ name, note }) => ({ value: name, label: name, note }));
    }

    get shown(): Variant {
        return this.variants.find((variant) => variant.name === chosen.get(this.label)) ?? this.#first;
    }

    choose(name: string): void {
        chosen.set(this.label, name);
    }

    /**
     * Chooses the variant in `slot`, when one of the variants is in it. Returns whether it chose
     * one.
     */
    chooseSlot(slot: string): boolean {
        const variant = this.variants.find((candidate) => candidate.slot === slot);
        if (variant === undefined) return false;
        this.choose(variant.name);
        return true;
    }
}
