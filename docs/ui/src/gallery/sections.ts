import { required } from "@/shared/required";

/**
 * Returns the tab names of the sections of the `/// gallery` block inside `host`, in order.
 */
export function tabsOf(host: HTMLElement): string[] {
    return [...host.querySelectorAll(":scope > section")].map(tabOf);
}

/**
 * Returns the section of the `/// gallery` block inside `host` that fills the panel at `index`.
 */
export function sectionOf(host: HTMLElement, index: number): Element {
    return required(host, "the gallery").child(`:scope > section[slot="panel-${index}"]`, `a section for panel ${index + 1}`);
}

function tabOf(section: Element, index: number): string {
    const heading = required(section, `gallery section ${index + 1}`).child(":scope > :is(h2, h3, h4):first-child", "a heading at its start");
    const textNodes = [...heading.childNodes].filter((node) => !(node instanceof Element && node.classList.contains("headerlink")));
    return textNodes
        .map((node) => node.textContent ?? "")
        .join("")
        .trim();
}
