<script lang="ts">
    let { label, active }: { label: string; active: boolean } = $props();
</script>

<span class="loading" role="status">
    <faran-mark class="mark" loading={active} label=""></faran-mark>
    <span class="label">{label}</span>
</span>

<style>
    .loading {
        display: inline-flex;
        align-items: center;
        gap: 0.6rem;
        color: var(--faran-text-muted, #b8afc6);
        font-family: var(--faran-font-text, system-ui, sans-serif);
        font-size: 0.7rem;
    }

    .mark {
        width: 1.6rem;
        flex: none;
    }
</style>
