import type { Frame } from "@engine";
import { proxy } from "comlink";
import { prefersReducedMotion } from "svelte/motion";
import { pythonAssetsUrl } from "@/shared/site";
import { ConnectedWorker, failureMessage } from "@/shared/worker";
import type { MapLayout } from "@/docsmap/layout";
import type { NavigationLayout, NavigationStep } from "@/docsmap/messages";
import { MotionPlayback } from "@/docsmap/playback";
import type { NavigationWorker } from "@/docsmap/worker";

const EMPTY_FRAME: Frame = { renderings: [], info: [] };

/**
 * Runs the docs map's planner in a web worker that `start` starts. Aiming at a place before the
 * planner is ready aims at it once it is.
 */
export class MapSession {
    background: Frame = $state.raw(EMPTY_FRAME);
    frame: Frame = $state.raw(EMPTY_FRAME);
    motion: Frame = $state.raw(EMPTY_FRAME);
    status = $state("");
    ready = $state(false);
    failed = $state(false);
    aimedAt = $state(-1);
    stepMilliseconds = $state(0);

    #worker: ConnectedWorker<NavigationWorker> | undefined = undefined;
    readonly #playback = new MotionPlayback((frame) => (this.motion = frame));
    readonly #showStatusProxy = proxy((text: string) => this.#showStatus(text));
    readonly #showStepProxy = proxy((step: NavigationStep) => this.#showStep(step));

    constructor(private readonly layout: MapLayout) {}

    /**
     * Starts the worker and loads Pyodide and Faran in it, unless that has already started.
     */
    start(): void {
        const hasStarted = this.#worker !== undefined;
        if (hasStarted) return;
        this.status = "Loading Faran in your browser…";
        this.#worker = startNavigationWorker();
        void this.#loadPlanner(this.#worker);
    }

    /**
     * Plans towards the place with the given index, where the last index is the start.
     */
    aim(index: number): void {
        if (index === this.aimedAt) return;
        this.aimedAt = index;
        this.start();
        if (this.ready) this.#sendAim();
    }

    stop(): void {
        this.#worker?.terminate();
        this.#playback.stop();
    }

    async #loadPlanner(worker: ConnectedWorker<NavigationWorker>): Promise<void> {
        const options = plannerOptions(this.layout);
        try {
            this.#becomeReady(await worker.call((exposed) => exposed.start(options, this.#showStatusProxy)));
        } catch (error: unknown) {
            this.#fail(failureMessage(error));
        }
    }

    #showStatus(text: string): void {
        this.status = `${text}…`;
    }

    #becomeReady(background: Frame): void {
        this.background = background;
        this.ready = true;
        this.status = "";
        const hasAimed = this.aimedAt >= 0;
        if (hasAimed) this.#sendAim();
    }

    #showStep({ frame, motion, milliseconds }: NavigationStep): void {
        this.frame = frame;
        this.#playback.play(motion);
        this.stepMilliseconds = milliseconds;
    }

    #sendAim(): void {
        const aim = { place: this.aimedAt, instantly: prefersReducedMotion.current };
        this.#connected()
            .call((worker) => worker.aim(aim, this.#showStepProxy))
            .catch((error: unknown) => this.#fail(failureMessage(error)));
    }

    #fail(message: string): void {
        this.failed = true;
        this.status = "The planner could not start in this browser.";
        console.error(`The docs map planner failed: ${message}`);
    }

    #connected(): ConnectedWorker<NavigationWorker> {
        if (this.#worker === undefined) throw new Error("The docs map planner was aimed before its worker started.");
        return this.#worker;
    }
}

function startNavigationWorker(): ConnectedWorker<NavigationWorker> {
    return new ConnectedWorker(new Worker(new URL("./worker.ts", import.meta.url), { type: "module" }));
}

function plannerOptions(layout: MapLayout): { assetsUrl: string; layout: NavigationLayout } {
    return { assetsUrl: pythonAssetsUrl(), layout: navigationLayout(layout) };
}

function navigationLayout({ height, places, obstacles, start }: MapLayout): NavigationLayout {
    const up = ([x, y]: readonly [number, number]) => [x, height - y] as const;
    return {
        places: [...places.map(up), up([start.x, start.y])],
        obstacles: obstacles.map(({ center, radius }) => ({ center: up(center), radius })),
        start: { x: start.x, y: height - start.y, heading: -start.heading },
    };
}
