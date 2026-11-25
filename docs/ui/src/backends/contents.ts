import { required } from "@/shared/required";
import { BACKENDS, type Backend } from "@/backends/choice.svelte";

const CLASS_NAME_PREFIXES: Record<Backend, string> = { NumPy: "NumPy", JAX: "Jax" };

/**
 * An item of the table of contents that links to the class documented in one backend's part of
 * a `<faran-backends>` element.
 */
export interface BackendEntry {
    readonly backend: Backend;
    readonly item: HTMLElement;
    readonly link: HTMLAnchorElement;
}

interface BackendPart {
    readonly backend: Backend;
    readonly element: HTMLElement;
}

/**
 * Returns the entries of `contents` that link to a class in a `<faran-backends>` element.
 */
export function findBackendEntries(contents: HTMLElement): BackendEntry[] {
    return backendParts().flatMap((part) => entriesFor({ contents, part }));
}

/**
 * Removes the backend prefix, such as `NumPy`, from the label of each entry.
 */
export function removeBackendPrefixes(entries: readonly BackendEntry[]): void {
    for (const entry of entries) removePrefix(entry);
}

function backendParts(): BackendPart[] {
    return [...document.querySelectorAll<HTMLElement>("faran-backends > [slot]")].map(partOf);
}

function partOf(element: HTMLElement): BackendPart {
    const backend = BACKENDS.find((candidate) => candidate === element.slot);
    if (backend === undefined) throw new Error(`Expected a part of a backends block to have one of the slots ${BACKENDS.join(", ")}, but it has "${element.slot}".`);
    return { backend, element };
}

function entriesFor({ contents, part }: { contents: HTMLElement; part: BackendPart }): BackendEntry[] {
    const links = linksTo({ contents, id: classHeadingIdOf(part) });
    return links.map((link) => ({ backend: part.backend, item: itemOf(link), link }));
}

function classHeadingIdOf(part: BackendPart): string {
    return required(part.element, `the ${part.backend} part of a backends block`).child(".doc-heading[id]", "the heading of a class").id;
}

function linksTo({ contents, id }: { contents: HTMLElement; id: string }): HTMLAnchorElement[] {
    return [...contents.querySelectorAll<HTMLAnchorElement>(`a.md-nav__link[href="#${CSS.escape(id)}"]`)];
}

function itemOf(link: HTMLAnchorElement): HTMLElement {
    return required(link, `the table of contents link ${link.href}`).ancestor<HTMLElement>(".md-nav__item", "an item");
}

function removePrefix({ backend, link }: BackendEntry): void {
    const label = labelTextOf(link);
    label.data = label.data.replace(CLASS_NAME_PREFIXES[backend], "");
}

function labelTextOf(link: HTMLAnchorElement): Text {
    const texts = [...(link.querySelector(".md-typeset") ?? link).childNodes].filter((node) => node instanceof Text);
    const label = texts.reverse().find((text) => text.data.trim() !== "");
    if (label === undefined) throw new Error(`Expected the table of contents link ${link.href} to have a text label, but it has none.`);
    return label;
}
