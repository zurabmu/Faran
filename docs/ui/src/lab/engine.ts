import { proxy } from "comlink";
import { LatestCall } from "@/shared/latest";
import { pythonAssetsUrl } from "@/shared/site";
import { ConnectedWorker, failureMessage } from "@/shared/worker";
import type { LabReceiver } from "@/lab/messages";
import type { LabWorker } from "@/lab/worker";

/**
 * Receives what the worker reports. Background, step and failure callbacks receive only what
 * belongs to the latest run.
 */
export interface LabCallbacks extends LabReceiver {
    onFailure(message: string): void;
}

/**
 * Runs Faran demos in a Pyodide web worker, which it starts on the first run.
 */
export class LabEngine {
    #worker: ConnectedWorker<LabWorker> | undefined;
    readonly #runs = new LatestCall();

    constructor(private readonly callbacks: LabCallbacks) {}

    /**
     * Starts a demo and replaces any demo that is running.
     *
     * @param demo Key of the `demos` mapping in `docs/lab/scenarios.py`.
     */
    run(demo: string): void {
        const isLatest = this.#runs.begin();
        const receiver = this.#receiverFor(isLatest);
        this.#connected()
            .call((worker) => worker.run({ demo, assetsUrl: pythonAssetsUrl() }, receiver))
            .catch((error: unknown) => {
                if (isLatest()) this.callbacks.onFailure(failureMessage(error));
            });
    }

    /**
     * Stops the running demo after its current planner step.
     */
    stop(): void {
        this.#runs.cancel();
        void this.#connected().call((worker) => worker.stop());
    }

    #receiverFor(isLatest: () => boolean): LabReceiver {
        const { callbacks } = this;
        return proxy<LabReceiver>({
            onStatus: (text) => callbacks.onStatus(text),
            onBackground: (background) => {
                if (isLatest()) callbacks.onBackground(background);
            },
            onStep: (step) => {
                if (isLatest()) callbacks.onStep(step);
            },
        });
    }

    #connected(): ConnectedWorker<LabWorker> {
        this.#worker ??= new ConnectedWorker(new Worker(new URL("./worker.ts", import.meta.url), { type: "module" }));
        return this.#worker;
    }
}
