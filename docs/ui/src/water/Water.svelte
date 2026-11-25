<svelte:options customElement={{ tag: "faran-water" }} />

<script lang="ts">
    import { startWaterOn } from "@/water/page";
</script>

<canvas aria-hidden="true" {@attach startWaterOn}></canvas>

<style>
    :host {
        position: fixed;
        inset: 0;
        z-index: 0;
        pointer-events: none;
    }

    canvas {
        display: block;
        width: 100%;
        height: 100%;
    }
</style>
