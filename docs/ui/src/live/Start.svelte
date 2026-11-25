<script lang="ts">
    import IconButton from "@/shared/IconButton.svelte";
    import { icons } from "@/shared/icons";

    let { status, onstart }: { status: string; onstart: () => void } = $props();
</script>

<div class="start">
    <IconButton class="start-button" label="Run code" icon={icons.play} onclick={onstart} />
    <p>{status}</p>
</div>

<style>
    .start {
        display: grid;
        place-content: center;
        justify-items: center;
        gap: 0.9rem;
        padding: 0 1.5rem;
        text-align: center;
    }

    .start :global(.start-button) {
        display: grid;
        place-items: center;
        width: 3.4rem;
        height: 3.4rem;
        padding: 0;
        border: 1px solid var(--faran-rule-strong, #3e3650);
        border-radius: 50%;
        background: none;
        color: var(--faran-text, #f1ecf4);
        cursor: pointer;
        transition:
            border-color 0.2s,
            color 0.2s;
    }

    .start :global(.start-button .icon) {
        width: 1.3rem;
        height: 1.3rem;
    }

    .start :global(.start-button:is(:hover, :focus-visible)) {
        border-color: var(--faran-start-text, #ffa487);
        color: var(--faran-start-text, #ffa487);
        outline: none;
    }

    p {
        max-width: 26rem;
        margin: 0;
        color: var(--faran-text-faint, #a59cb5);
        font-size: 0.66rem;
    }

    @media (prefers-reduced-motion: reduce) {
        .start :global(.start-button) {
            transition: none;
        }
    }
</style>
