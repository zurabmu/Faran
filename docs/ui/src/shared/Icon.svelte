<script lang="ts">
    let { path }: { path: string } = $props();
</script>

<svg class="icon" viewBox="0 0 16 16" aria-hidden="true"><path d={path} /></svg>

<style>
    .icon {
        flex: none;
        width: 0.85rem;
        height: 0.85rem;
        fill: none;
        stroke: currentcolor;
        stroke-linecap: round;
        stroke-linejoin: round;
        stroke-width: 1.5;
    }
</style>
