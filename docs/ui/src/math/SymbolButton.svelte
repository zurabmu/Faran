<script lang="ts">
    import type { LegendSymbol } from "@/math/content";
    import { copiesOf } from "@/shared/dom/copies";
    import type { LegendSelection } from "@/math/selection.svelte";

    let { symbol, index, selection }: { symbol: LegendSymbol; index: number; selection: LegendSelection } = $props();

    function clearOnEscape(event: KeyboardEvent): void {
        if (event.key === "Escape") selection.clear();
    }
</script>

<button
    type="button"
    class:shown={selection.shown === index}
    aria-label={symbol.source}
    aria-describedby="symbol-{index}"
    onpointerenter={() => selection.hover(index)}
    onpointerleave={() => selection.leave()}
    onclick={() => selection.select(index)}
    onfocus={() => selection.select(index)}
    onkeydown={clearOnEscape}
    {@attach copiesOf([symbol.notation])}
></button>

<style>
    button {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        min-width: 2.2rem;
        min-height: 2rem;
        padding: 0 0.55rem;
        border: 1px solid var(--faran-rule-strong, #3e3650);
        border-radius: 2px;
        background-color: var(--faran-bg, #0f0d17);
        color: var(--faran-text, #f1ecf4);
        cursor: help;
        transition:
            border-color 0.12s,
            color 0.12s;
    }

    button.shown {
        border-color: var(--faran-end, #c28bff);
        color: var(--faran-end-text, #ffd8c2);
    }

    button:focus-visible {
        outline: 2px solid var(--faran-end-text, #ffd8c2);
        outline-offset: 2px;
    }

    button :global(.katex) {
        color: inherit;
        font-size: 1em;
    }

    @media (pointer: coarse) {
        button {
            min-width: 2.75rem;
            min-height: 2.75rem;
        }
    }

    @media (prefers-reduced-motion: reduce) {
        button {
            transition: none;
        }
    }
</style>
