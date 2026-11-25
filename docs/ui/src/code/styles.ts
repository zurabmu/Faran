/**
 * How one kind of Python token is drawn. `name` is both the class of the editor's marks and the
 * name of the CSS highlight.
 */
export interface CodeStyle {
    readonly name: string;
    readonly color: string;
    readonly fontStyle: string;
}

/**
 * The site's code colors by token kind, shared by the editor and the code blocks on the page.
 */
export const codeStyles = {
    keyword: { name: "faran-code-keyword", color: "var(--faran-code-keyword, #ffa487)", fontStyle: "normal" },
    literal: { name: "faran-code-literal", color: "var(--faran-code-literal, #ffd2c2)", fontStyle: "normal" },
    function: { name: "faran-code-function", color: "var(--faran-code-function, #b9bbff)", fontStyle: "normal" },
    comment: { name: "faran-code-comment", color: "var(--faran-code-comment, #a59cb5)", fontStyle: "italic" },
    syntax: { name: "faran-code-syntax", color: "var(--faran-code-syntax, #b8afc6)", fontStyle: "normal" },
    argument: { name: "faran-code-argument", color: "var(--faran-code-quiet, #8d849e)", fontStyle: "normal" },
} as const satisfies Record<string, CodeStyle>;

/**
 * Every code style, in no particular order.
 */
export const CODE_STYLES: readonly CodeStyle[] = Object.values(codeStyles);
