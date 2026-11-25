<script lang="ts">
    import IconButton from "@/shared/IconButton.svelte";
    import { icons } from "@/shared/icons";
    import type { PlayerControls } from "@/shared/player/controls";

    let { player }: { player: PlayerControls } = $props();
</script>

<span class="buttons">
    <IconButton class="step" label="Go to start" icon={icons.toStart} disabled={!player.ready} onclick={() => player.seek(player.first)} />
    <IconButton class="step" label="Previous step" icon={icons.stepBack} disabled={!player.ready} onclick={() => player.stepBy(-1)} />
    <IconButton
        class="play"
        label={player.playing ? "Pause" : "Play"}
        icon={player.playing ? icons.pause : icons.play}
        disabled={!player.ready}
        onclick={() => player.toggle()}
    />
    <IconButton class="step" label="Next step" icon={icons.stepForward} disabled={!player.ready} onclick={() => player.stepBy(1)} />
</span>

<style>
    .buttons {
        display: contents;
    }

    .buttons :global(button) {
        display: grid;
        place-items: center;
        padding: 0;
        border: 1px solid transparent;
        border-radius: 2px;
        background: none;
        color: var(--faran-text-muted, #b8afc6);
        cursor: pointer;
    }

    .buttons :global(button .icon) {
        fill: currentcolor;
    }

    .buttons :global(.step) {
        width: 1.6rem;
        height: 1.6rem;
    }

    .buttons :global(.step:is(:hover, :focus-visible):enabled) {
        color: var(--faran-text, #f1ecf4);
        background-color: var(--faran-raised, #1f1b2a);
    }

    .buttons :global(.play) {
        width: 2.1rem;
        height: 2.1rem;
        margin: 0 0.15rem;
        border-color: var(--faran-rule-strong, #3e3650);
        border-radius: 50%;
        color: var(--faran-text, #f1ecf4);
    }

    .buttons :global(.play .icon) {
        width: 0.95rem;
        height: 0.95rem;
    }

    .buttons :global(.play:is(:hover, :focus-visible):enabled) {
        border-color: var(--faran-start-text, #ffa487);
        color: var(--faran-start-text, #ffa487);
    }

    .buttons :global(button:focus-visible) {
        outline: 2px solid var(--faran-end-text, #a3a6ff);
        outline-offset: 2px;
    }

    .buttons :global(button:disabled) {
        cursor: default;
        opacity: 0.5;
    }

    @media (pointer: coarse) {
        .buttons :global(:is(.step, .play)) {
            width: 2.75rem;
            height: 2.75rem;
        }
    }
</style>
