<script lang="ts">
    import Clock from "@/shared/player/Clock.svelte";
    import type { PlayerControls } from "@/shared/player/controls";
    import Scrubber from "@/shared/player/Scrubber.svelte";
    import Speed from "@/shared/player/Speed.svelte";
    import StepButtons from "@/shared/player/StepButtons.svelte";

    let { player }: { player: PlayerControls } = $props();
</script>

<div class="transport">
    <div class="layout">
        <span class="buttons"><StepButtons {player} /></span>
        <span class="scrubber"><Scrubber {player} /></span>
        <span class="readouts">
            <Clock step={player.step} last={player.last} seconds={player.seconds} endSeconds={player.endSeconds} />
            <Speed speed={player.speed} disabled={!player.ready} onchange={(speed) => player.changeSpeed(speed)} />
        </span>
    </div>
</div>

<style>
    .transport {
        flex: 1 1 18rem;
        min-width: 0;
        container-type: inline-size;
    }

    .layout {
        display: grid;
        grid-template-areas: "buttons scrubber readouts";
        grid-template-columns: auto minmax(6rem, 1fr) auto;
        align-items: center;
        gap: 0.6rem 0.9rem;
    }

    .buttons {
        display: flex;
        grid-area: buttons;
        align-items: center;
        gap: 0.15rem;
    }

    .scrubber {
        display: flex;
        grid-area: scrubber;
    }

    .readouts {
        display: flex;
        flex-wrap: wrap;
        grid-area: readouts;
        justify-content: flex-end;
        gap: 0.4rem;
    }

    @container (max-width: 34rem) {
        .layout {
            grid-template-areas:
                "scrubber scrubber"
                "buttons readouts";
            grid-template-columns: auto 1fr;
        }
    }

    @container (max-width: 24rem) {
        .layout {
            grid-template-areas:
                "scrubber"
                "buttons"
                "readouts";
            grid-template-columns: 1fr;
        }

        .readouts {
            justify-content: flex-start;
        }
    }
</style>
