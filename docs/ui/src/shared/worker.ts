import { type Remote, releaseProxy, wrap } from "comlink";

/**
 * The object that a web worker exposes with Comlink. A call also rejects when the worker fails
 * outside of any call.
 */
export class ConnectedWorker<Exposed> {
    readonly #worker: Worker;
    readonly #exposed: Remote<Exposed>;
    readonly #failure: Promise<never>;

    constructor(worker: Worker) {
        this.#worker = worker;
        this.#exposed = wrap<Exposed>(worker);
        this.#failure = new Promise((_, reject) => worker.addEventListener("error", ({ message }) => reject(new Error(message))));
        // A failure of the worker matters only to the calls that wait for it.
        this.#failure.catch(() => undefined);
    }

    call<Result>(calling: (exposed: Remote<Exposed>) => Promise<Result>): Promise<Result> {
        return Promise.race([calling(this.#exposed), this.#failure]);
    }

    terminate(): void {
        this.#exposed[releaseProxy]();
        this.#worker.terminate();
    }
}

/**
 * Returns the message of an error that a worker call rejected with.
 */
export function failureMessage(error: unknown): string {
    return error instanceof Error ? error.message : String(error);
}
