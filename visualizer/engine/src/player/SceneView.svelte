<script lang="ts">
    import type { Rendering } from "@engine/animation";
    import { SceneCanvas } from "@engine/scene";
    import type { Bounds } from "@engine/view";

    const SCENE_PADDING = 24;

    let { renderings, bounds }: { renderings: readonly Rendering[]; bounds: Bounds } = $props();

    function attachScene(canvas: HTMLCanvasElement): () => void {
        const scene = SceneCanvas.on(canvas);
        $effect(() => scene.draw({ renderings, bounds, padding: SCENE_PADDING }));
        return () => scene.dispose();
    }
</script>

<canvas {@attach attachScene}></canvas>

<style>
    canvas {
        position: absolute;
        inset: 0;
        display: block;
        width: 100%;
        height: 100%;
    }
</style>
