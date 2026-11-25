import { required } from "@/shared/required";

/**
 * Returns the entry in the page's reference list that the citation link inside `host` points to.
 */
export function referenceOf(host: HTMLElement): Element {
    const link = required(host, `the citation ${host.textContent}`).child<HTMLAnchorElement>("a", "a link");
    const id = decodeURIComponent(link.hash.slice(1));
    return required(document.documentElement, "the page").child(`#${CSS.escape(id)}`, `the reference list entry ${id}`);
}
