import { fileURLToPath } from "node:url";
import { svelte } from "@sveltejs/vite-plugin-svelte";
import { defineConfig } from "vite";

export default defineConfig({
    plugins: [svelte({ compilerOptions: { css: "injected" } })],
    resolve: {
        alias: [
            { find: /^@faran\/engine$/, replacement: fileURLToPath(new URL("./src/index.ts", import.meta.url)) },
            { find: /^@\/(.*)$/, replacement: `${fileURLToPath(new URL("./src/", import.meta.url))}$1` },
            { find: /^@test\/(.*)$/, replacement: `${fileURLToPath(new URL("./tests/", import.meta.url))}$1` },
        ],
    },
    build: {
        outDir: "../faran_visualizer/renderers/canvas",
        emptyOutDir: false,
        lib: {
            entry: "src/index.ts",
            name: "FaranCanvas",
            formats: ["iife"],
            fileName: () => "engine.js",
        },
    },
});
