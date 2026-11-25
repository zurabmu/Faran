<script lang="ts">
    let { status, entries }: { status: string; entries: readonly string[] } = $props();
</script>

<span class="readout" aria-live="polite">
    <span>{status}</span>
    {#each entries as entry, index (index)}
        <span>{entry}</span>
    {/each}
</span>

<style>
    .readout {
        display: flex;
        flex-wrap: wrap;
        gap: 0.2rem 0.9rem;
        font-family: var(--faran-font-code, ui-monospace, monospace);
        font-size: 0.62rem;
    }
</style>
