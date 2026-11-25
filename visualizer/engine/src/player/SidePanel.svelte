<script lang="ts">
    import uPlotStyles from "uplot/dist/uPlot.min.css?raw";
    import type { Chart, Row } from "@engine/animation";
    import ChartFigure from "@engine/player/ChartFigure.svelte";
    import { formatValue } from "@engine/player/format";

    let { rows, charts, step, seek }: { rows: readonly Row[]; charts: readonly Chart[]; step: number; seek: (step: number) => void } = $props();

    function valueWithUnit(row: Row): string {
        const value = formatValue(row.value);
        const hasUnit = row.unit !== "";
        return hasUnit ? `${value} ${row.unit}` : value;
    }
</script>

<aside class="side">
    {@html `<style>${uPlotStyles}</style>`}
    <table>
        <tbody>
            {#each rows as row (row.label)}
                <tr>
                    <td>{row.label}</td>
                    <td>{valueWithUnit(row)}</td>
                </tr>
            {/each}
        </tbody>
    </table>
    {#each charts as chart (chart.id)}
        <ChartFigure {chart} {step} {seek} />
    {/each}
</aside>

<style>
    .side {
        display: flex;
        flex-direction: column;
        gap: 0.9rem;
        min-height: 0;
        padding: 0.8rem 0.9rem;
        overflow-y: auto;
        border-left: 1px solid var(--rule);
        background: var(--surface);
    }

    table {
        width: 100%;
        border-collapse: collapse;
        font-variant-numeric: tabular-nums;
    }

    td {
        padding: 0.15rem 0;
    }

    td:first-child {
        color: var(--muted);
    }

    td:last-child {
        text-align: right;
    }

    @container faran-animation (max-width: 40rem) {
        .side {
            border-left: none;
            border-top: 1px solid var(--rule);
        }
    }
</style>
