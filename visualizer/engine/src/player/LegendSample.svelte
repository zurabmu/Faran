<script lang="ts">
    import type { LineMark, Mark } from "@/animation";
    import { cssColor, dashesFor } from "@/style";

    const WIDTH = 28;
    const HEIGHT = 14;
    const LINE_INSET = 2;

    let { marks }: { marks: readonly Mark[] } = $props();

    function dashArrayOf(mark: LineMark): string | undefined {
        const dashes = dashesFor(mark.pattern, mark.width);
        const isSolid = dashes.length === 0;
        return isSolid ? undefined : dashes.join(" ");
    }
</script>

<svg viewBox="0 0 {WIDTH} {HEIGHT}" width={WIDTH} height={HEIGHT} aria-hidden="true">
    {#each marks as mark, index (index)}
        {#if mark.kind === "line"}
            <line
                x1={LINE_INSET}
                y1={HEIGHT / 2}
                x2={WIDTH - LINE_INSET}
                y2={HEIGHT / 2}
                stroke={cssColor(mark.color)}
                stroke-width={mark.width}
                stroke-dasharray={dashArrayOf(mark)}
            />
        {:else}
            <circle cx={WIDTH / 2} cy={HEIGHT / 2} r={mark.size / 2} fill={cssColor(mark.color)} />
        {/if}
    {/each}
</svg>

<style>
    svg {
        flex: none;
        overflow: visible;
    }
</style>
