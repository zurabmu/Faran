<script lang="ts">
    import type { Snippet } from "svelte";

    let { title, children }: { title: string; children: Snippet } = $props();
</script>

<section class="frame" aria-label={title}>{@render children()}</section>

<style>
    .frame {
        display: flex;
        flex-direction: column;
        box-sizing: border-box;
        height: 100%;
        margin: 0;
        border: 1px solid var(--faran-rule, #2b2636);
        border-radius: 2px;
        background-color: var(--faran-surface, #17141f);
        color: var(--faran-text, #f1ecf4);
        font-family: var(--faran-font-text, system-ui, sans-serif);
    }
</style>
