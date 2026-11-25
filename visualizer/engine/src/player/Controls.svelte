<script lang="ts">
    import type { Playback } from "@engine/playback.svelte";

    let { playback }: { playback: Playback } = $props();

    const lastStep = $derived(playback.stepCount - 1);
    const progressPercent = $derived((playback.step / Math.max(1, lastStep)) * 100);
    const seconds = $derived((playback.step * playback.timeStep).toFixed(1));
</script>

<div class="controls">
    <button type="button" class="play" aria-label={playback.playing ? "Pause" : "Play"} onclick={() => playback.toggle()}>
        <svg viewBox="0 0 16 16" aria-hidden="true">
            {#if playback.playing}
                <path d="M5.5 3.5v9M10.5 3.5v9" />
            {:else}
                <path d="M5 3.2v9.6L12.6 8z" />
            {/if}
        </svg>
    </button>
    <input
        type="range"
        min="0"
        max={lastStep}
        value={playback.step}
        aria-label="Step"
        style:--progress="{progressPercent}%"
        oninput={(event) => playback.seek(Number(event.currentTarget.value))}
    />
    <span class="readout">Step {playback.step} of {lastStep}, {seconds} s</span>
</div>

<style>
    .controls {
        display: flex;
        grid-column: 1 / -1;
        align-items: center;
        gap: 0.8rem;
        padding: 0.5rem 0.9rem;
        border-top: 1px solid var(--rule);
        background: var(--surface);
    }

    .play {
        display: grid;
        flex: none;
        place-items: center;
        width: 1.8rem;
        height: 1.8rem;
        padding: 0;
        border: 1px solid var(--rule-strong);
        border-radius: 50%;
        background: none;
        color: var(--text);
        cursor: pointer;
    }

    .play:is(:hover, :focus-visible) {
        border-color: var(--accent);
        color: var(--accent);
    }

    .play svg {
        width: 0.8rem;
        height: 0.8rem;
        fill: currentcolor;
        stroke: currentcolor;
        stroke-linecap: round;
        stroke-linejoin: round;
        stroke-width: 1.6;
    }

    input {
        flex: 1;
        height: 1rem;
        margin: 0;
        background: none;
        cursor: pointer;
        appearance: none;
    }

    input::-webkit-slider-runnable-track {
        height: 1px;
        background: linear-gradient(90deg, var(--accent) var(--progress), var(--rule-strong) var(--progress));
    }

    input::-moz-range-track {
        height: 1px;
        background: var(--rule-strong);
    }

    input::-moz-range-progress {
        height: 1px;
        background: var(--accent);
    }

    input::-webkit-slider-thumb {
        width: 0.65rem;
        height: 0.65rem;
        margin-top: calc(-0.325rem + 0.5px);
        border: none;
        border-radius: 50%;
        background: var(--accent);
        appearance: none;
    }

    input::-moz-range-thumb {
        width: 0.65rem;
        height: 0.65rem;
        border: none;
        border-radius: 50%;
        background: var(--accent);
    }

    .readout {
        flex: none;
        min-width: 7.5rem;
        color: var(--muted);
        font-variant-numeric: tabular-nums;
        text-align: right;
    }

    @container faran-animation (max-width: 40rem) {
        .controls {
            grid-row: 2;
        }
    }
</style>
