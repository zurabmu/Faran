<script lang="ts">
    import type { Snippet } from "svelte";

    let { edge, children }: { edge: "top" | "bottom"; children: Snippet } = $props();
</script>

<div class="bar {edge}">{@render children()}</div>

<style>
    .bar {
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        gap: 0.5rem 1.2rem;
        padding: 0.5rem 0.9rem;
        color: var(--faran-text-muted, #b8afc6);
        font-size: 0.68rem;
    }

    .top {
        border-bottom: 1px solid var(--faran-rule, #2b2636);
    }

    .bottom {
        border-top: 1px solid var(--faran-rule, #2b2636);
    }
</style>
