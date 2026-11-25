import { indentWithTab } from "@codemirror/commands";
import { python } from "@codemirror/lang-python";
import { EditorView, keymap, lineNumbers } from "@codemirror/view";
import { minimalSetup } from "codemirror";
// Imported past the `code` entry module, which the page loads up front, so that CodeMirror stays in this lazily loaded chunk.
import { codeHighlighting } from "@/code/editor";

const siteTheme = EditorView.theme(
    {
        "&": {
            backgroundColor: "var(--faran-code-bg, #14111c)",
            color: "var(--faran-code-name, #ece5ef)",
            fontSize: "0.72rem",
        },
        ".cm-content": { fontFamily: "var(--faran-font-code, ui-monospace, monospace)", caretColor: "var(--faran-text, #f1ecf4)" },
        ".cm-scroller": { fontFamily: "var(--faran-font-code, ui-monospace, monospace)", lineHeight: "1.6" },
        ".cm-gutters": { backgroundColor: "transparent", color: "var(--faran-code-quiet, #8d849e)", border: "none" },
        ".cm-activeLine, .cm-activeLineGutter": { backgroundColor: "var(--faran-end-wash, rgba(127, 131, 240, 0.14))" },
        "&.cm-focused .cm-selectionBackground, .cm-selectionBackground": { backgroundColor: "rgba(127, 131, 240, 0.3)" },
        "&.cm-focused": { outline: "none" },
    },
    { dark: true },
);

/**
 * A Python editor in the site's code colors.
 */
export interface SnippetEditor {
    readonly source: string;
    reset(): void;
    destroy(): void;
}

/**
 * Creates an editor for `source` inside `parent`. Resetting restores `source`.
 */
export function createEditor({ parent, source }: { parent: HTMLElement; source: string }): SnippetEditor {
    const view = new EditorView({
        doc: source,
        parent,
        extensions: [minimalSetup, lineNumbers(), keymap.of([indentWithTab]), python(), siteTheme, codeHighlighting],
    });
    return {
        get source() {
            return view.state.doc.toString();
        },
        reset() {
            view.dispatch({ changes: { from: 0, to: view.state.doc.length, insert: source } });
        },
        destroy() {
            view.destroy();
        },
    };
}
