import { highlightTree, type Tag, tagHighlighter, tags } from "@lezer/highlight";
import type { SyntaxNodeRef, Tree } from "@lezer/common";
import { type CodeStyle, codeStyles } from "@/code/styles";

/**
 * A piece of Python source, by character offsets, and the style it is drawn in.
 */
export interface CodeSpan {
    readonly from: number;
    readonly to: number;
    readonly style: CodeStyle;
}

const TAG_STYLES: readonly { readonly tags: Tag[]; readonly style: CodeStyle }[] = [
    { tags: [tags.keyword, tags.bool, tags.null], style: codeStyles.keyword },
    { tags: [tags.string, tags.number], style: codeStyles.literal },
    { tags: [tags.function(tags.variableName), tags.function(tags.propertyName)], style: codeStyles.function },
    { tags: [tags.comment], style: codeStyles.comment },
    { tags: [tags.operator, tags.punctuation], style: codeStyles.syntax },
];

const highlighter = tagHighlighter(TAG_STYLES.map(({ tags }, index) => ({ tag: tags, class: String(index) })));

/**
 * Returns the styled spans of a Python syntax tree from `@lezer/python`, ordered by position and
 * not overlapping. Text outside the spans is drawn plain.
 */
export function codeSpans(tree: Tree): CodeSpan[] {
    const spans: CodeSpan[] = [];
    highlightTree(tree, highlighter, (from, to, classes) => spans.push({ from, to, style: styleOfClass(classes) }));
    tree.iterate({
        enter: (node) => {
            if (isKeywordArgumentName(node)) spans.push({ from: node.from, to: node.to, style: codeStyles.argument });
        },
    });
    return spans.sort((first, second) => first.from - second.from);
}

function styleOfClass(classes: string): CodeStyle {
    const entry = TAG_STYLES[Number(classes)];
    if (entry === undefined) throw new Error(`Expected the highlighter class "${classes}" to index a code style, but it does not.`);
    return entry.style;
}

function isKeywordArgumentName(node: SyntaxNodeRef): boolean {
    const isArgumentName = node.name === "VariableName" && node.node.parent?.name === "ArgList";
    return isArgumentName && node.node.nextSibling?.name === "AssignOp";
}
