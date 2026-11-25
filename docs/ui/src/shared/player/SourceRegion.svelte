<script lang="ts">
    import type { Snippet } from "svelte";
    import type { SourcePanel } from "@/shared/player/source.svelte";

    let { panel, children }: { panel: SourcePanel; children: Snippet } = $props();
</script>

<div class="source" class:open={panel.open} inert={!panel.open}>
    <div class="inner">
        {#if panel.requested}
            {@render children()}
        {/if}
    </div>
</div>

<style>
    .source {
        display: grid;
        grid-template-rows: 0fr;
        border-top: 1px solid transparent;
        transition:
            grid-template-rows 0.45s cubic-bezier(0.22, 0.61, 0.36, 1),
            border-color 0.45s;
    }

    .source.open {
        grid-template-rows: 1fr;
        border-top-color: var(--faran-rule, #2b2636);
    }

    :global(.expanded) .source.open {
        flex: 0 0 40%;
        min-height: 0;
    }

    .inner {
        min-height: 0;
        overflow: hidden;
    }

    .inner > :global(*),
    .inner :global(::slotted(*)) {
        max-height: 28rem;
        margin: 0 !important;
        overflow: auto;
    }

    :global(.expanded) .inner > :global(*),
    :global(.expanded) .inner :global(::slotted(*)) {
        height: 100%;
        max-height: none;
    }

    @media (prefers-reduced-motion: reduce) {
        .source {
            transition: none;
        }
    }
</style>
