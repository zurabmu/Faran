/**
 * One variant of a `<faran-variants>` element: its name, a short note that describes it, and the
 * slot that holds its content.
 */
export interface Variant {
    readonly name: string;
    readonly note: string;
    readonly slot: string;
}

/**
 * Reads the variants of the `/// variants` block inside `host`, in order.
 */
export function readVariants(host: HTMLElement): Variant[] {
    return [...host.querySelectorAll<HTMLElement>(":scope > [slot^='variant-']")].map(variantOf);
}

function variantOf(element: HTMLElement): Variant {
    const { name, note } = element.dataset;
    if (name === undefined || note === undefined) throw new Error(`Expected the variant in slot ${element.slot} to have data-name and data-note attributes.`);
    return { name, note, slot: element.slot };
}
