import { syntaxHighlighting, syntaxTree } from "@codemirror/language";
import { RangeSetBuilder } from "@codemirror/state";
import { tagHighlighter } from "@lezer/highlight";
import { Decoration, type DecorationSet, EditorView, ViewPlugin, type ViewUpdate } from "@codemirror/view";
import { codeSpans } from "@/code/spans";
import { CODE_STYLES } from "@/code/styles";

const marks = new Map(CODE_STYLES.map((style) => [style, Decoration.mark({ class: style.name })]));

const markColors = EditorView.baseTheme(Object.fromEntries(CODE_STYLES.map(({ name, color, fontStyle }) => [`.${name}`, { color, fontStyle }])));

const markPlugin = ViewPlugin.fromClass(
    class {
        decorations: DecorationSet;

        constructor(view: EditorView) {
            this.decorations = decorationsOf(view);
        }

        update(update: ViewUpdate): void {
            const treeChanged = syntaxTree(update.state) !== syntaxTree(update.startState);
            if (update.docChanged || treeChanged) this.decorations = decorationsOf(update.view);
        }
    },
    { decorations: (plugin) => plugin.decorations },
);

/**
 * CodeMirror extensions that color Python code with the site's code styles. Requires the
 * `python()` language.
 */
export const codeHighlighting = [markPlugin, markColors, withoutDefaultHighlighting()];

function withoutDefaultHighlighting() {
    // CodeMirror applies its default highlight style only while no other highlighter is active.
    return syntaxHighlighting(tagHighlighter([]));
}

function decorationsOf(view: EditorView): DecorationSet {
    const builder = new RangeSetBuilder<Decoration>();
    for (const { from, to, style } of codeSpans(syntaxTree(view.state))) {
        const mark = marks.get(style);
        if (mark === undefined) throw new Error(`Expected the code style "${style.name}" to be one of CODE_STYLES, but it is not.`);
        builder.add(from, to, mark);
    }
    return builder.finish();
}
