import type { CodeSpan } from "@/code/spans";
import { CODE_STYLES, type CodeStyle } from "@/code/styles";
import { BlockText } from "@/code/text";

interface ColoredRange {
    readonly highlight: Highlight;
    readonly range: Range;
}

/** One CSS highlight per code style. */
export class StyleHighlights {
    private readonly highlights = new Map<CodeStyle, Highlight>(CODE_STYLES.map((style) => [style, new Highlight()]));

    /** Recolors `code` whenever the theme replaces its text nodes. */
    colorBlock(code: HTMLElement, spans: readonly CodeSpan[]): void {
        let colored = this.color(code, spans);
        const recolor = () => {
            this.uncolor(colored);
            colored = this.color(code, spans);
        };
        new MutationObserver(recolor).observe(code, { childList: true, subtree: true, characterData: true });
    }

    applyToDocument(): void {
        for (const [style, highlight] of this.highlights) {
            CSS.highlights.set(style.name, highlight);
        }
        adoptHighlightColors();
    }

    private color(code: HTMLElement, spans: readonly CodeSpan[]): ColoredRange[] {
        const text = new BlockText(code);
        return spans.map((span) => {
            const colored = { highlight: this.highlightOf(span.style), range: text.rangeOf(span) };
            colored.highlight.add(colored.range);
            return colored;
        });
    }

    private uncolor(colored: readonly ColoredRange[]): void {
        for (const { highlight, range } of colored) highlight.delete(range);
    }

    private highlightOf(style: CodeStyle): Highlight {
        const highlight = this.highlights.get(style);
        if (highlight === undefined) throw new Error(`Expected the code style "${style.name}" to be one of CODE_STYLES, but it is not.`);
        return highlight;
    }
}

function adoptHighlightColors(): void {
    const sheet = new CSSStyleSheet();
    sheet.replaceSync(CODE_STYLES.map(({ name, color }) => `::highlight(${name}) { color: ${color}; }`).join("\n"));
    document.adoptedStyleSheets = [...document.adoptedStyleSheets, sheet];
}
