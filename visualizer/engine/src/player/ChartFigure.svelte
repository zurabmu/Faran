<script lang="ts">
    import type { Chart } from "@engine/animation";
    import { ChartPlot, chartThemeOf } from "@engine/player/charts";
    import { ChartReadout } from "@engine/player/readout.svelte";
    import { sizeWatcherOf } from "@engine/size";

    let { chart, step, seek }: { chart: Chart; step: number; seek: (step: number) => void } = $props();

    const hasYLabel = $derived(chart.yLabel !== "");
    const readout = new ChartReadout(() => chart);
    const isHovered = $derived(readout.readings.length > 0);

    function attachPlot(area: HTMLElement): () => void {
        const pointer = { hover: (step: number) => readout.hover(step), leave: () => readout.leave(), seek };
        const plot = new ChartPlot({ container: area, chart, theme: chartThemeOf(area), watchSize: sizeWatcherOf(area), pointer });
        $effect(() => plot.show(step));
        return () => plot.destroy();
    }
</script>

<figure>
    <figcaption>{hasYLabel ? chart.yLabel : chart.title}</figcaption>
    <p class="readout">
        {#if isHovered}
            <span>Step {readout.step}</span>
            {#each readout.readings as reading (reading.name)}
                <span style:color={reading.color}>{reading.name} {reading.value}</span>
            {/each}
        {/if}
    </p>
    <div class="chart" {@attach attachPlot}></div>
</figure>

<style>
    figure {
        margin: 0;
    }

    figcaption {
        margin-bottom: 0.25rem;
        color: var(--muted);
        font-size: 12px;
    }

    .readout {
        display: flex;
        flex-wrap: wrap;
        gap: 0 0.6rem;
        min-height: 1.45em;
        margin: 0 0 0.25rem;
        color: var(--muted);
        font-size: 11px;
        font-variant-numeric: tabular-nums;
    }

    .chart {
        height: 7.5rem;
    }

    .chart :global(.u-over) {
        cursor: pointer;
        touch-action: none;
    }

    .chart :global(.u-cursor-x) {
        border-right-color: var(--faint);
    }
</style>
