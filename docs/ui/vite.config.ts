import { svelte, vitePreprocess } from "@sveltejs/vite-plugin-svelte";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { defineConfig } from "vite";

const RERUN_VIEWER = "@rerun-io/web-viewer";
const rerunViewerVersion: string = JSON.parse(readFileSync(new URL(`node_modules/${RERUN_VIEWER}/package.json`, import.meta.url), "utf8")).version;

export default defineConfig({
    plugins: [svelte({ preprocess: vitePreprocess(), compilerOptions: { customElement: true } })],
    resolve: {
        // The canvas engine and the water surface share one copy of three.js.
        dedupe: ["three"],
        alias: [
            { find: /^@\/(.*)$/, replacement: `${fileURLToPath(new URL("./src/", import.meta.url))}$1` },
            { find: /^@engine$/, replacement: fileURLToPath(new URL("../../visualizer/engine/src/index.ts", import.meta.url)) },
            { find: /^@engine\/(.*)$/, replacement: `${fileURLToPath(new URL("../../visualizer/engine/src/", import.meta.url))}$1` },
        ],
    },
    base: "./",
    worker: { format: "es" },
    build: {
        outDir: "../content/javascripts/ui",
        emptyOutDir: true,
        lib: {
            entry: { index: "src/index.ts", viewer: "src/replay/viewer/index.ts" },
            formats: ["es"],
            fileName: (_format, entry) => `${entry}.js`,
        },
        rollupOptions: {
            // The viewer's wasm module is 70 MB, so the replay page loads it from a CDN instead of the site.
            external: [RERUN_VIEWER],
            output: { paths: { [RERUN_VIEWER]: `https://unpkg.com/${RERUN_VIEWER}@${rerunViewerVersion}/index.js` } },
        },
    },
});
