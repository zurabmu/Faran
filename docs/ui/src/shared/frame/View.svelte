<script lang="ts">
    import type { Snippet } from "svelte";

    let { children }: { children: Snippet } = $props();
</script>

<div class="view">{@render children()}</div>

<style>
    .view {
        position: relative;
        flex: 1;
        min-height: 0;
        background-color: var(--faran-bg, #0f0d17);
    }
</style>
