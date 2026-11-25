<script lang="ts">
    let { message }: { message: string } = $props();
</script>

{#if message !== ""}
    <pre class="failure">{message}</pre>
{/if}

<style>
    .failure {
        max-height: 16rem;
        margin: 0;
        padding: 0.6rem 0.9rem;
        overflow: auto;
        border-top: 1px solid var(--faran-rule, #2b2636);
        background-color: var(--faran-raised, #1f1b2a);
        color: var(--faran-start-text, #ffa487);
        font-family: var(--faran-font-code, ui-monospace, monospace);
        font-size: 0.62rem;
        white-space: pre-wrap;
    }
</style>
