import { writeFileSync } from "node:fs";
import { join } from "node:path";
import { faviconSvg } from "@/favicon/drawing";
import { loadingSpinnerSvg } from "@/loading/spinner";
import { markSvg } from "@/mark/static";
import { icoFile, renderPng } from "./icons";

const ASSETS = join(import.meta.dirname, "..", "..", "content", "assets");

function write(name: string, content: string | Buffer): void {
    writeFileSync(join(ASSETS, name), content);
    console.log(`Wrote docs/content/assets/${name}`);
}

const favicon = faviconSvg({ tile: true });
write("logo.svg", markSvg());
write("logo-mark.svg", faviconSvg({ tile: false }));
write("favicon.svg", favicon);
write("favicon.ico", await icoFile(favicon, [16, 32, 48]));
write("apple-touch-icon.png", renderPng(favicon, 180));
write("loading.svg", loadingSpinnerSvg());
