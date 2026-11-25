<script lang="ts">
    import { type PlayerControls, progressOf } from "@/shared/player/controls";

    let { player }: { player: PlayerControls } = $props();
</script>

<input
    type="range"
    class="scrubber"
    aria-label="Step"
    aria-valuetext="Step {player.step} of {player.last}, {player.seconds.toFixed(2)} seconds"
    min={player.first}
    max={player.last}
    value={player.step}
    disabled={!player.ready}
    style:--progress="{progressOf(player)}%"
    oninput={(event) => player.seek(Number(event.currentTarget.value))}
/>

<style>
    .scrubber {
        width: 100%;
        height: 1.4rem;
        margin: 0;
        background: none;
        cursor: pointer;
        appearance: none;
    }

    .scrubber:disabled {
        cursor: default;
    }

    .scrubber:focus-visible {
        outline: none;
    }

    .scrubber::-webkit-slider-runnable-track {
        height: 3px;
        border-radius: 2px;
        background: linear-gradient(90deg, var(--faran-start-text, #ffa487) var(--progress), var(--faran-rule-strong, #3e3650) var(--progress));
    }

    .scrubber::-moz-range-track {
        height: 3px;
        border-radius: 2px;
        background-color: var(--faran-rule-strong, #3e3650);
    }

    .scrubber::-moz-range-progress {
        height: 3px;
        border-radius: 2px;
        background-color: var(--faran-start-text, #ffa487);
    }

    .scrubber::-webkit-slider-thumb {
        width: 0.8rem;
        height: 0.8rem;
        margin-top: calc(-0.4rem + 1.5px);
        border: 2px solid var(--faran-surface, #17141f);
        border-radius: 50%;
        background-color: var(--faran-start-text, #ffa487);
        transition: transform 0.15s;
        appearance: none;
    }

    .scrubber::-moz-range-thumb {
        width: 0.8rem;
        height: 0.8rem;
        box-sizing: border-box;
        border: 2px solid var(--faran-surface, #17141f);
        border-radius: 50%;
        background-color: var(--faran-start-text, #ffa487);
        transition: transform 0.15s;
    }

    .scrubber:is(:hover, :focus-visible):enabled::-webkit-slider-thumb {
        transform: scale(1.3);
    }

    .scrubber:is(:hover, :focus-visible):enabled::-moz-range-thumb {
        transform: scale(1.3);
    }

    @media (prefers-reduced-motion: reduce) {
        .scrubber::-webkit-slider-thumb {
            transition: none;
        }

        .scrubber::-moz-range-thumb {
            transition: none;
        }
    }
</style>
