import type { Bounds, Frame, Rendering } from "@engine";
import { FIRST_RUN_DOWNLOADS } from "@/shared/python";
import { LabEngine } from "@/lab/engine";
import type { LabStep } from "@/lab/messages";

/**
 * The demos that `docs/lab/scenarios.py` defines, in the order the lab offers them.
 */
export const demos = [
    { value: "path-following", label: "Path following" },
    { value: "corridor", label: "Corridor" },
    { value: "obstacle-avoidance", label: "Obstacles" },
] as const;

const EMPTY_FRAME: Frame = { renderings: [], info: [] };
const UNIT_BOUNDS: Bounds = { left: 0, bottom: 0, right: 1, top: 1 };

/**
 * The state of the lab: the demo it runs, what the run reports, and what it draws.
 */
export class LabSession {
    demo = $state<string>(demos[0].value);
    running = $state(false);
    status = $state(FIRST_RUN_DOWNLOADS);
    failure = $state("");
    readout = $state.raw<readonly string[]>([]);
    background = $state.raw<Frame>(EMPTY_FRAME);
    bounds = $state.raw<Bounds>(UNIT_BOUNDS);
    moving = $state.raw<Frame>(EMPTY_FRAME);

    readonly #engine = new LabEngine({
        onStatus: (text) => this.#showStatus(text),
        onBackground: (background) => void this.#showBackground(background),
        onStep: (step) => this.#showStep(step),
        onFailure: (message) => this.#fail(message),
    });

    /**
     * Whether a demo has sent what it draws.
     */
    get isDrawable(): boolean {
        return this.background.renderings.length > 0;
    }

    get renderings(): readonly Rendering[] {
        return [...this.background.renderings, ...this.moving.renderings];
    }

    select(demo: string): void {
        this.demo = demo;
        if (this.running) this.#start();
    }

    toggle(): void {
        if (this.running) this.#stop();
        else this.#start();
    }

    #start(): void {
        this.running = true;
        this.failure = "";
        this.readout = [];
        this.status = "Starting";
        this.#engine.run(this.demo);
    }

    #stop(): void {
        this.#engine.stop();
        this.#finish("Stopped");
    }

    #finish(status: string): void {
        this.status = status;
        this.running = false;
    }

    #showStatus(text: string): void {
        if (this.running) this.status = text;
    }

    async #showBackground(background: Frame): Promise<void> {
        const { boundsOf } = await import("@engine");
        this.bounds = boundsOf(background.renderings);
        this.background = background;
        this.moving = EMPTY_FRAME;
    }

    #showStep(step: LabStep): void {
        this.moving = step.frame;
        this.readout = readoutOf(step);
        if (step.finished) this.#finish(finishStatusOf(step));
    }

    #fail(message: string): void {
        this.#finish("Failed");
        this.failure = message;
    }
}

function readoutOf(step: LabStep): string[] {
    return [
        `Step ${step.step}`,
        `${Math.round(step.progress * 100)}% of goal`,
        `${step.speed.toFixed(1)} m/s`,
        `${step.planningMilliseconds.toFixed(0)} ms per plan`,
    ];
}

function finishStatusOf(step: LabStep): string {
    return step.reachedGoal ? "Reached the goal" : "Reached the step limit";
}
