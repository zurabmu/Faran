import type { CodeSpan } from "@/code/spans";

/**
 * The text nodes of a code block, by the character offset where each one starts.
 */
export class BlockText {
    private readonly nodes: Text[] = [];
    private readonly starts: number[] = [];

    constructor(code: HTMLElement) {
        const walker = document.createTreeWalker(code, NodeFilter.SHOW_TEXT);
        let start = 0;
        for (let node = walker.nextNode(); node !== null; node = walker.nextNode()) {
            this.nodes.push(node as Text);
            this.starts.push(start);
            start += (node as Text).length;
        }
    }

    /**
     * Returns the DOM range of the span's characters.
     */
    rangeOf({ from, to }: CodeSpan): Range {
        const range = new Range();
        range.setStart(...this.pointAt(from));
        range.setEnd(...this.pointAt(to));
        return range;
    }

    private pointAt(offset: number): [Text, number] {
        const index = this.lastNodeStartingAtOrBefore(offset);
        const node = this.nodes[index];
        const start = this.starts[index];
        if (node === undefined || start === undefined) throw new Error(`Expected the code block to have text at offset ${offset}, but it has none.`);
        return [node, offset - start];
    }

    private lastNodeStartingAtOrBefore(offset: number): number {
        let low = 0;
        let high = this.starts.length - 1;
        while (low < high) {
            const middle = Math.ceil((low + high) / 2);
            if ((this.starts[middle] ?? Infinity) <= offset) low = middle;
            else high = middle - 1;
        }
        return low;
    }
}
