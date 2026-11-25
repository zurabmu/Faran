import type { Drawing } from "@engine";

/**
 * Draws on `canvas` with the canvas engine, which it loads on the first call. Draws again
 * whenever the drawing that `drawing` returns changes. Returns a function that releases the
 * canvas.
 */
export function drawScene(canvas: HTMLCanvasElement, drawing: () => Drawing): () => void {
    const scene = import("@engine").then(({ SceneCanvas }) => SceneCanvas.on(canvas));
    $effect(() => {
        const current = drawing();
        void scene.then((engine) => engine.draw(current));
    });
    return () => void scene.then((engine) => engine.dispose());
}
