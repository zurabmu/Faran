import type { Frame } from "@engine";
import { interpolateFrames } from "@/docsmap/interpolation";
import { type Motion, STEP_MILLISECONDS } from "@/docsmap/messages";

const SMOOTHING = 0.2;
const PAUSE_FACTOR = 4;

/**
 * Plays the motion of each planner step until the next step arrives.
 */
export class MotionPlayback {
    #motion: Motion = { start: { renderings: [], info: [] }, end: { renderings: [], info: [] } };
    #startedAt = 0;
    #stepMilliseconds = STEP_MILLISECONDS;
    #animationFrame = 0;

    constructor(private readonly show: (frame: Frame) => void) {}

    /**
     * Starts showing the motion of a new step, from its start.
     */
    play(motion: Motion): void {
        const now = performance.now();
        this.#measureStepTime(now - this.#startedAt);
        this.#motion = motion;
        this.#startedAt = now;
        cancelAnimationFrame(this.#animationFrame);
        this.#showAt(now);
    }

    stop(): void {
        cancelAnimationFrame(this.#animationFrame);
    }

    #measureStepTime(sinceLastStep: number): void {
        const wasPaused = sinceLastStep > this.#stepMilliseconds * PAUSE_FACTOR;
        if (wasPaused) return;
        this.#stepMilliseconds += (sinceLastStep - this.#stepMilliseconds) * SMOOTHING;
    }

    #showAt(time: number): void {
        const fraction = Math.min(1, Math.max(0, (time - this.#startedAt) / this.#stepMilliseconds));
        this.show(interpolateFrames(this.#motion.start, this.#motion.end, fraction));
        if (fraction < 1) this.#animationFrame = requestAnimationFrame((next) => this.#showAt(next));
    }
}
