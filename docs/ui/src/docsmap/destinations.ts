import { required } from "@/shared/required";
import type { Destination } from "@/docsmap/layout";

/**
 * Reads the destinations from the list of the `/// docs-map` block inside `host`.
 */
export function destinationsOf(host: HTMLElement): Destination[] {
    return [...host.querySelectorAll(":scope > ul > li")].map(destinationOf);
}

function destinationOf(item: Element): Destination {
    const link = required(item, `the docs map item "${item.textContent}"`).child<HTMLAnchorElement>("a", "a link");
    const title = link.textContent ?? "";
    const description = (item.textContent ?? "").slice(title.length).replace(/^\s*:\s*/, "").trim();
    return { title, href: link.href, description };
}
