<script lang="ts">
    import type { LegendEntry } from "@/animation";
    import LegendSample from "@/player/LegendSample.svelte";

    let { entries, open }: { entries: readonly LegendEntry[]; open: boolean } = $props();
</script>

{#if entries.length > 0}
    <details class="legend" {open}>
        <summary>Legend</summary>
        <ul>
            {#each entries as entry (entry.label)}
                <li>
                    <LegendSample marks={entry.marks} />
                    <span>{entry.label}</span>
                </li>
            {/each}
        </ul>
    </details>
{/if}

<style>
    .legend {
        position: absolute;
        top: 0.6rem;
        left: 0.6rem;
        max-width: calc(100% - 1.2rem);
        max-height: calc(100% - 1.2rem);
        overflow-y: auto;
        border: 1px solid var(--rule);
        border-radius: 4px;
        background: color-mix(in srgb, var(--surface) 88%, transparent);
        backdrop-filter: blur(6px);
        font-size: 12px;
    }

    summary {
        display: flex;
        align-items: center;
        gap: 0.45rem;
        padding: 0.3rem 0.6rem;
        color: var(--muted);
        cursor: pointer;
        list-style: none;
        user-select: none;
    }

    summary::-webkit-details-marker {
        display: none;
    }

    summary::before {
        width: 0.32rem;
        height: 0.32rem;
        border-right: 1.5px solid currentcolor;
        border-bottom: 1.5px solid currentcolor;
        content: "";
        transform: translateY(-0.1rem) rotate(45deg);
        transition: transform 120ms ease-out;
    }

    .legend:not([open]) summary::before {
        transform: rotate(-45deg);
    }

    summary:is(:hover, :focus-visible) {
        color: var(--text);
    }

    summary:focus-visible {
        outline: 1px solid var(--accent);
        outline-offset: -1px;
        border-radius: 4px;
    }

    ul {
        display: grid;
        gap: 0.25rem;
        margin: 0;
        padding: 0.05rem 0.7rem 0.55rem;
        list-style: none;
    }

    li {
        display: flex;
        align-items: center;
        gap: 0.55rem;
        color: var(--text);
        white-space: nowrap;
    }

    @media (prefers-reduced-motion: reduce) {
        summary::before {
            transition: none;
        }
    }
</style>
