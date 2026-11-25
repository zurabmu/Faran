import { cpSync } from "node:fs";
import { createRequire } from "node:module";
import { dirname, join } from "node:path";

const DIST = dirname(createRequire(import.meta.url).resolve("katex"));
const TARGET = join(import.meta.dirname, "..", "..", "content", "assets", "katex");

function isNotLegacyFont(path: string): boolean {
    return !/\.(woff|ttf)$/.test(path);
}

cpSync(join(DIST, "katex.min.css"), join(TARGET, "katex.min.css"));
cpSync(join(DIST, "fonts"), join(TARGET, "fonts"), { recursive: true, filter: isNotLegacyFont });
cpSync(join(DIST, "..", "LICENSE"), join(TARGET, "LICENSE"));
console.log("Wrote docs/content/assets/katex/");
