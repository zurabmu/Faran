import katex from "katex";

/**
 * Typesets the Arithmatex formulas under `root` that are not typeset yet. A formula that KaTeX
 * rejects is logged and shown as an error.
 */
export function typesetMath(root: ParentNode): void {
    for (const element of root.querySelectorAll<HTMLElement>(".arithmatex:not(.faran-typeset)")) {
        typesetFormula(element);
    }
}

function typesetFormula(element: HTMLElement): void {
    const source = stripDelimiters(element.textContent ?? "");
    const displayMode = element.tagName === "DIV";

    try {
        katex.render(source, element, { displayMode, throwOnError: true });
    } catch (error) {
        console.error(`KaTeX could not typeset "${source}" on ${location.pathname}: ${(error as Error).message}`);
        katex.render(source, element, { displayMode, throwOnError: false });
    }

    element.classList.add("faran-typeset");
}

function stripDelimiters(text: string): string {
    return text.trim().slice(2, -2);
}
