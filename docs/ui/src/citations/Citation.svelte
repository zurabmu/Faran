<svelte:options customElement={{ tag: "faran-citation" }} />

<script lang="ts">
    import { CitationCard } from "@/citations/card.svelte";

    const id = $props.id();
    const card = new CitationCard({ id, host: $host() });
</script>

<span class="citation" {...card.api.getTriggerProps()} {@attach card.root.attach} {@attach card.openOnFocus}
    ><slot /><span class="positioner" popover="manual" {...card.api.getPositionerProps()} {@attach card.showWhileOpen}
        ><aside class="card" role="tooltip" {...card.api.getContentProps()} {@attach card.showReference}></aside></span
    ></span>

<style>
    .positioner {
        inset: auto;
        margin: 0;
        padding: 0;
        border: none;
        background: none;
        overflow: visible;
    }

    .card {
        display: grid;
        grid-template-columns: 2.2em minmax(0, 1fr);
        box-sizing: border-box;
        width: min(24rem, calc(100vw - 16px));
        margin: 0;
        padding: 0.8rem 1rem;
        border: 1px solid var(--faran-rule-strong, #3e3650);
        border-left: 2px solid var(--faran-start-text, #ffa487);
        border-radius: 2px;
        background-color: var(--faran-surface, #17141f);
        box-shadow: 0 0.8rem 2rem rgba(4, 3, 8, 0.55);
        color: var(--faran-text, #f1ecf4);
        font-family: var(--faran-font-text, system-ui, sans-serif);
        font-size: 0.72rem;
        line-height: 1.5;
        animation: open 0.42s var(--faran-ease-water, ease-out) both;
    }

    .card :global(.faran-reference__label) {
        color: var(--faran-text-faint, #a59cb5);
        font-variant-numeric: tabular-nums;
    }

    .card :global(a) {
        color: inherit;
        text-decoration: underline;
        text-decoration-color: var(--faran-rule-strong, #3e3650);
        text-underline-offset: 0.2em;
        overflow-wrap: anywhere;
    }

    @keyframes open {
        from {
            clip-path: circle(0 at var(--transform-origin));
        }

        to {
            clip-path: circle(150% at var(--transform-origin));
        }
    }

    @media (prefers-reduced-motion: reduce) {
        .card {
            animation: none;
        }
    }
</style>
