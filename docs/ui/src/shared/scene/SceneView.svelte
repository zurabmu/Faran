<script lang="ts">
    import type { Bounds, Rendering } from "@engine";
    import { drawScene } from "@/shared/scene/drawing.svelte";

    let { renderings, bounds, padding }: { renderings: readonly Rendering[]; bounds: Bounds; padding: number } = $props();
</script>

<canvas aria-hidden="true" {@attach (canvas) => drawScene(canvas, () => ({ renderings, bounds, padding }))}></canvas>

<style>
    canvas {
        display: block;
        width: 100%;
        height: 100%;
    }
</style>
