<script lang="ts">
    import { copiesOf } from "@/shared/dom/copies";
    import type { EquationLegend } from "@/math/equation-legend.svelte";
    import SymbolButton from "@/math/SymbolButton.svelte";

    let { legend }: { legend: EquationLegend } = $props();
</script>

<div class="legend">
    <div class="symbols" role="group" aria-label="Symbols">
        {#each legend.symbols as symbol, index (index)}
            <SymbolButton {symbol} {index} selection={legend.selection} />
        {/each}
    </div>
    <div class="notes">
        <p class="hint" hidden={!legend.selection.isEmpty}>Hover, tap or focus a symbol to see what it stands for.</p>
        {#each legend.symbols as symbol, index (index)}
            <p class="note" id="symbol-{index}" hidden={legend.selection.shown !== index} {@attach copiesOf(symbol.note)}></p>
        {/each}
    </div>
</div>

<style>
    .legend {
        padding: 0.7rem 1.2rem 0.8rem;
        border-top: 1px solid var(--faran-rule, #2b2636);
    }

    .symbols {
        display: flex;
        flex-wrap: wrap;
        gap: 0.4rem;
    }

    .notes {
        min-height: 1.65em;
        margin-top: 0.6rem;
        font-size: 0.9em;
    }

    .notes p {
        margin: 0;
    }

    .hint {
        color: var(--faran-text-faint, #a59cb5);
    }

    .note {
        color: var(--faran-text-muted, #c9c0d4);
    }

    .note :global(.katex) {
        color: var(--faran-text, #f1ecf4);
        font-size: 1.08em;
    }
</style>
