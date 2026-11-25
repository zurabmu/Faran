<script lang="ts">
    let { text }: { text: string } = $props();
</script>

<span class="title">{text}</span>

<style>
    .title {
        color: var(--faran-text, #f1ecf4);
        font-size: 0.72rem;
        font-weight: 600;
    }
</style>
