import { required } from "@/shared/required";

const ATOM_CLASSES = ["mord", "mop", "mbin", "mrel", "mopen", "mclose", "mpunct", "minner"];
const SEPARATOR_CLASSES = ["mopen", "mclose", "mpunct"];

/**
 * Returns the atoms of `formula` where `notation` occurs. Both must be typeset by KaTeX. A tuple
 * occurs wherever each of its parts occurs.
 */
export function occurrencesOf({ formula, notation }: { formula: Element; notation: Element }): Element[] {
    return partsOf(notation).flatMap((part) => findPart({ formula, part }));
}

function partsOf(notation: Element): string[][] {
    const parts: string[][] = [[]];
    for (const atom of [...notation.querySelectorAll(".katex-html > .katex-base > *")].filter(isAtom)) {
        if (isSeparator(atom)) parts.push([]);
        else parts.at(-1)?.push(visibleText(atom));
    }
    return parts.filter((part) => part.length > 0);
}

function findPart({ formula, part }: { formula: Element; part: readonly string[] }): Element[] {
    const containers = formula.querySelectorAll(".katex-html, .katex-html *");
    const runs = [...containers].flatMap((container) => runsIn({ atoms: [...container.children].filter(isAtom), part }));
    return runs.filter((run) => !runs.some((other) => other !== run && encloses(run, other))).flat();
}

function runsIn({ atoms, part }: { atoms: readonly Element[]; part: readonly string[] }): Element[][] {
    return atoms
        .map((_, start) => atoms.slice(start, start + part.length))
        .filter((run) => run.length === part.length && run.every((atom, index) => readingsOf(atom).includes(part[index] ?? "")));
}

function readingsOf(atom: Element): string[] {
    const scripts = atom.querySelector(":scope > .msupsub");
    if (scripts === null) return [visibleText(atom)];
    const base = [...atom.children]
        .filter((child) => child !== scripts)
        .map(visibleText)
        .join("");
    return [visibleText(atom), base + subscriptOf(scripts)];
}

function subscriptOf(scripts: Element): string {
    const rows = required(scripts, `the KaTeX scripts of "${visibleText(scripts)}"`).child(":scope > .vlist-t", "a .vlist-t row");
    const subscript = rows.querySelector(":scope > .vlist-r:first-child > .vlist > span");
    const hasSubscript = rows.classList.contains("vlist-t2") && subscript !== null;
    return hasSubscript ? visibleText(subscript) : "";
}

function encloses(run: readonly Element[], other: readonly Element[]): boolean {
    return run.some((atom) => other.some((inner) => atom !== inner && atom.contains(inner)));
}

function isAtom(node: Element): boolean {
    return ATOM_CLASSES.some((name) => node.classList.contains(name));
}

function isSeparator(atom: Element): boolean {
    return SEPARATOR_CLASSES.some((name) => atom.classList.contains(name));
}

function visibleText(node: Element): string {
    const rendered = node.querySelector(".katex-html") ?? node;
    return (rendered.textContent ?? "").replace(/​/g, "").trim();
}
