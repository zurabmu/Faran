import type { Playback } from "@engine";
import type { PlayerControls } from "@/shared/player/controls";

/**
 * Player controls for an animation of the canvas engine. It is not ready until `connect` gives
 * it a playback.
 */
export class AnimationPlayer implements PlayerControls {
    readonly first = 0;
    ready = $state(false);
    playing = $state(false);
    step = $state(0);
    last = $state(0);
    seconds = $state(0);
    endSeconds = $state(0);
    speed = $state(1);

    #playback: Playback | undefined = undefined;

    /**
     * Mirrors and drives `playback`, at the speed picked so far. Returns a function that disconnects it.
     */
    connect(playback: Playback): () => void {
        this.#playback = playback;
        playback.speed = this.speed;
        const mirror = () => {
            this.ready = true;
            this.playing = playback.playing;
            this.step = playback.step;
            this.last = playback.stepCount - 1;
            this.seconds = playback.step * playback.timeStep;
            this.endSeconds = this.last * playback.timeStep;
        };
        mirror();
        const stopMirroring = playback.onChange(mirror);
        return () => {
            stopMirroring();
            this.#playback = undefined;
            this.ready = false;
        };
    }

    toggle(): void {
        this.#connected().toggle();
    }

    seek(step: number): void {
        this.#connected().seek(step);
    }

    stepBy(count: number): void {
        this.seek(this.step + count);
    }

    changeSpeed(speed: number): void {
        this.speed = speed;
        this.#connected().speed = speed;
    }

    #connected(): Playback {
        if (this.#playback === undefined) throw new Error("The animation player is not connected to a playback.");
        return this.#playback;
    }
}
