import type { CodeSpan } from "@/code/spans";
import { CODE_STYLES, type CodeStyle } from "@/code/styles";
import type { BlockText } from "@/code/text";

/**
 * The ranges to color with each code style, collected over several code blocks.
 */
export class StyleHighlights {
    private readonly ranges = new Map<CodeStyle, Range[]>(CODE_STYLES.map((style) => [style, []]));

    /**
     * Adds the ranges of `spans` in the code block whose text is `text`.
     */
    addSpans(spans: readonly CodeSpan[], text: BlockText): void {
        for (const span of spans) {
            this.rangesOf(span.style).push(text.rangeOf(span));
        }
    }

    /**
     * Colors the collected ranges on the page.
     */
    applyToDocument(): void {
        for (const [style, ranges] of this.ranges) {
            CSS.highlights.set(style.name, new Highlight(...ranges));
        }
        adoptHighlightColors();
    }

    private rangesOf(style: CodeStyle): Range[] {
        const ranges = this.ranges.get(style);
        if (ranges === undefined) throw new Error(`Expected the code style "${style.name}" to be one of CODE_STYLES, but it is not.`);
        return ranges;
    }
}

function adoptHighlightColors(): void {
    const sheet = new CSSStyleSheet();
    sheet.replaceSync(CODE_STYLES.map(({ name, color }) => `::highlight(${name}) { color: ${color}; }`).join("\n"));
    document.adoptedStyleSheets = [...document.adoptedStyleSheets, sheet];
}
