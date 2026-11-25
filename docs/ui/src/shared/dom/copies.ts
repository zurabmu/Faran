import type { Attachment } from "svelte/attachments";

/**
 * Returns an attachment that fills its element with copies of `nodes`, so that markup of the
 * page shows inside a shadow root while the page keeps the originals.
 */
export function copiesOf(nodes: readonly Node[]): Attachment<HTMLElement> {
    return (target) => target.replaceChildren(...nodes.map((node) => node.cloneNode(true)));
}
