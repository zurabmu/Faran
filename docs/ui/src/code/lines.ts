import { Text } from "@codemirror/state";

/**
 * A class to add to one line of a code block, by zero-based line index.
 */
export interface LineMark {
    readonly line: number;
    readonly className: string;
}

/**
 * The lines of a source text, by zero-based line index.
 */
export class SourceLines {
    private readonly text: Text;

    constructor(source: string) {
        this.text = Text.of(source.split("\n"));
    }

    /**
     * Returns the index of the line that holds the character at `offset`.
     */
    at(offset: number): number {
        return this.text.lineAt(offset).number - 1;
    }

    /**
     * Returns the indices of the lines from the one at `from` to the one at `to`.
     */
    spannedBy({ from, to }: { from: number; to: number }): number[] {
        const first = this.at(from);
        return Array.from({ length: this.at(to) - first + 1 }, (_, index) => first + index);
    }
}

/**
 * Adds the class of each mark to the line span of its line. Throws when the code block has no
 * span for a marked line.
 */
export function markLines(code: HTMLElement, marks: readonly LineMark[]): void {
    const lines = code.querySelectorAll(":scope > span[id^='__span']");
    for (const { line, className } of marks) {
        const element = lines[line];
        if (element === undefined) throw new Error(`Expected the code block "${code.parentElement?.id}" to have a line span for line ${line + 1}, but it has ${lines.length}.`);
        element.classList.add(className);
    }
}
