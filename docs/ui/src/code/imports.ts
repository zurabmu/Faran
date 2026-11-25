import type { SyntaxNode, Tree } from "@lezer/common";
import { type LineMark, SourceLines } from "@/code/lines";

/**
 * Returns `faran-import` marks for the lines of the leading import statements and a
 * `faran-after-imports` mark for the first line after them. Comments and docstrings may come
 * before or between the imports.
 */
export function importLineMarks(tree: Tree, source: string): LineMark[] {
    const lines = new SourceLines(source);
    const statements = codeStatements(tree);
    const importCount = leadingImportCount(statements);
    const hasImports = importCount > 0;
    if (!hasImports) return [];

    const imports = statements.slice(0, importCount);
    const firstAfterImports = statements.slice(importCount, importCount + 1);
    return [
        ...imports.flatMap((statement) => lines.spannedBy(statement).map((line) => ({ line, className: "faran-import" }))),
        ...firstAfterImports.map((statement) => ({ line: lines.at(statement.from), className: "faran-after-imports" })),
    ];
}

function codeStatements(tree: Tree): SyntaxNode[] {
    const statements: SyntaxNode[] = [];
    for (let statement = tree.topNode.firstChild; statement !== null; statement = statement.nextSibling) {
        if (!isPreamble(statement)) statements.push(statement);
    }
    return statements;
}

function leadingImportCount(statements: readonly SyntaxNode[]): number {
    const firstOther = statements.findIndex((statement) => statement.name !== "ImportStatement");
    const allAreImports = firstOther === -1;
    return allAreImports ? statements.length : firstOther;
}

function isPreamble(statement: SyntaxNode): boolean {
    return statement.name === "Comment" || isDocstring(statement);
}

function isDocstring(statement: SyntaxNode): boolean {
    return statement.name === "ExpressionStatement" && statement.firstChild?.name === "String" && statement.firstChild.nextSibling === null;
}
