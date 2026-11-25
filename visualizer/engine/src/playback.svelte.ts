import { type FrameClock, screenFrames } from "@engine/frames";
import { StepTimer } from "@engine/timer";

/**
 * Steps through an animation, one step every `timeStep` seconds of real time at the playback
 * speed. Playing from the last step starts over. Time passes by the frames of `clock`.
 */
export class Playback {
    readonly stepCount: number;
    readonly timeStep: number;
    readonly #clock: FrameClock;
    #step = $state(0);
    #playing = $state(false);
    #speed = 1;
    #cancelNextFrame = () => {};
    #listeners: (() => void)[] = [];

    /**
     * `clock` defaults to the frames the browser paints.
     */
    constructor({ stepCount, timeStep, clock = screenFrames }: { stepCount: number; timeStep: number; clock?: FrameClock }) {
        if (stepCount < 1) throw new Error(`Expected an animation with at least one step, but it has ${stepCount}.`);
        this.stepCount = stepCount;
        this.timeStep = timeStep;
        this.#clock = clock;
    }

    get step(): number {
        return this.#step;
    }

    get playing(): boolean {
        return this.#playing;
    }

    /**
     * The playback speed, as a multiple of real time.
     */
    get speed(): number {
        return this.#speed;
    }

    set speed(speed: number) {
        if (!(speed > 0)) throw new Error(`Expected a positive playback speed, but got ${speed}.`);
        this.#speed = speed;
    }

    /**
     * Calls `listener` after every change of the step or of playing. Returns a function that stops
     * calling it.
     */
    onChange(listener: () => void): () => void {
        this.#listeners.push(listener);
        return () => {
            this.#listeners = this.#listeners.filter((candidate) => candidate !== listener);
        };
    }

    play(): void {
        if (this.#playing) return;
        if (this.#atLastStep) this.#step = 0;
        this.#playing = true;
        this.#requestFrame(new StepTimer({ timeStep: this.timeStep, startTime: this.#clock.now() }));
        this.#notify();
    }

    pause(): void {
        this.#stop();
        this.#notify();
    }

    toggle(): void {
        if (this.#playing) this.pause();
        else this.play();
    }

    /**
     * Pauses and moves to `step`, clamped to the steps of the animation.
     */
    seek(step: number): void {
        this.#stop();
        this.#step = this.#clampToSteps(Math.round(step));
        this.#notify();
    }

    get #lastStep(): number {
        return this.stepCount - 1;
    }

    get #atLastStep(): boolean {
        return this.#step >= this.#lastStep;
    }

    #clampToSteps(step: number): number {
        return Math.min(this.#lastStep, Math.max(0, step));
    }

    #requestFrame(timer: StepTimer): void {
        this.#cancelNextFrame = this.#clock.onNextFrame((time) => this.#showFrameAt(time, timer));
    }

    #showFrameAt(time: number, timer: StepTimer): void {
        const steps = timer.stepsDueAt(time, { speed: this.#speed });
        if (steps > 0) this.#advanceBy(steps);
        if (this.#playing) this.#requestFrame(timer);
    }

    #advanceBy(steps: number): void {
        this.#step = this.#clampToSteps(this.#step + steps);
        if (this.#atLastStep) this.#playing = false;
        this.#notify();
    }

    #stop(): void {
        this.#cancelNextFrame();
        this.#playing = false;
    }

    #notify(): void {
        for (const listener of this.#listeners) listener();
    }
}
