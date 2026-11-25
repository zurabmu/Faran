import { parser } from "@lezer/python";
import { StyleHighlights } from "@/code/highlights";
import { importLineMarks } from "@/code/imports";
import { markLines } from "@/code/lines";
import { codeSpans } from "@/code/spans";
import { BlockText } from "@/code/text";

const PYTHON_BLOCKS = ".language-python.highlight code";

/**
 * Colors the Python code blocks under `root`, marks their import lines and adds
 * `faran-highlighted` to each. Does nothing without the CSS Custom Highlight API. Expects the
 * line spans that `pymdownx.highlight` writes with `line_spans`.
 */
export function highlightCodeBlocks(root: ParentNode): void {
    const supportsHighlights = "highlights" in CSS;
    if (!supportsHighlights) return;

    const highlights = new StyleHighlights();
    for (const code of root.querySelectorAll<HTMLElement>(PYTHON_BLOCKS)) {
        highlightBlock(code, highlights);
    }
    highlights.applyToDocument();
}

function highlightBlock(code: HTMLElement, highlights: StyleHighlights): void {
    const source = code.textContent ?? "";
    const tree = parser.parse(source);
    highlights.addSpans(codeSpans(tree), new BlockText(code));
    markLines(code, importLineMarks(tree, source));
    code.classList.add("faran-highlighted");
}
