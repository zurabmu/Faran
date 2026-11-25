import { required } from "@/shared/required";

/**
 * A symbol of an equation's legend: its typeset notation, its TeX source, and the nodes of the
 * sentence that says what it stands for, which start with the notation.
 */
export interface LegendSymbol {
    readonly notation: Element;
    readonly source: string;
    readonly note: readonly Node[];
}

/**
 * Returns the display formula that an `/// equation` block holds inside `host`.
 */
export function formulaOf(host: HTMLElement): Element {
    return required(host, `the equation ${host.id}`).child(':scope > [slot="formula"]', "a display formula");
}

/**
 * Returns the symbols of the `/// equation` block inside `host`, in order.
 */
export function symbolsOf(host: HTMLElement): LegendSymbol[] {
    return [...host.querySelectorAll(':scope > [slot="symbols"] > li')].map((item) => symbolOf(host, item));
}

function symbolOf(host: HTMLElement, item: Element): LegendSymbol {
    const symbol = required(item, `the symbol "${item.textContent}" of the equation ${host.id}`);
    const notation = symbol.child(":scope > .arithmatex:first-child", "inline math at its start");
    const source = symbol.child('annotation[encoding="application/x-tex"]', "the TeX source that KaTeX keeps when it typesets");
    return { notation, source: (source.textContent ?? "").trim(), note: [...item.childNodes] };
}
