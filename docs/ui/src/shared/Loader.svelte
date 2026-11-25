<script lang="ts">
    let { label, active }: { label: string; active: boolean } = $props();
</script>

<div class="loader" role="status">
    <div class="center">
        <faran-mark class="mark" loading={active} label=""></faran-mark>
        <span class="label">{label}</span>
    </div>
</div>

<style>
    .loader {
        position: absolute;
        inset: 0;
        display: grid;
        place-content: center;
        background-color: var(--faran-bg, #0f0d17);
        color: var(--faran-text-muted, #b8afc6);
        font-family: var(--faran-font-text, system-ui, sans-serif);
        font-size: 0.7rem;
    }

    .center {
        position: relative;
    }

    .mark {
        display: block;
        width: 2.4rem;
    }

    .label {
        position: absolute;
        top: calc(100% + 0.8rem);
        left: 50%;
        translate: -50% 0;
        white-space: nowrap;
    }
</style>
