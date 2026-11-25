import type { Attachment } from "svelte/attachments";

/**
 * The root node of a component's elements, which is the shadow root inside a custom element.
 * It is the document until `attach` runs on one of the elements.
 */
export class RootNode {
    #node: Node = document;

    readonly get = (): Node => this.#node;

    readonly attach: Attachment<Element> = (element) => {
        this.#node = element.getRootNode();
    };
}
