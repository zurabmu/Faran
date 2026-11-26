import { type Remote, releaseProxy, wrap } from "comlink";

/**
 * The object that a web worker exposes. A call also rejects when the worker fails outside of any
 * call, and never settles once the worker is terminated.
 */
export class ConnectedWorker<Exposed> {
    readonly #worker: Worker;
    readonly #exposed: Remote<Exposed>;
    readonly #failure: Promise<never>;
    #terminated = false;

    constructor(worker: Worker) {
        this.#worker = worker;
        this.#exposed = wrap<Exposed>(worker);
        this.#failure = new Promise((_, reject) => worker.addEventListener("error", ({ message }) => reject(new Error(message))));
        // A failure of the worker matters only to the calls that wait for it.
        this.#failure.catch(() => undefined);
    }

    call<Result>(calling: (exposed: Remote<Exposed>) => Promise<Result>): Promise<Result> {
        return new Promise((resolve, reject) => {
            Promise.race([calling(this.#exposed), this.#failure]).then(
                (result) => {
                    if (!this.#terminated) resolve(result);
                },
                (error: unknown) => {
                    if (!this.#terminated) reject(error);
                },
            );
        });
    }

    terminate(): void {
        this.#terminated = true;
        this.#exposed[releaseProxy]();
        this.#worker.terminate();
    }
}

/**
 * A web worker that stops while the page is in the back/forward cache and starts again when the
 * page is shown.
 */
export class RestartingWorker<Exposed> {
    #worker: ConnectedWorker<Exposed> | undefined;
    #restartOnReturn = false;

    constructor(private readonly options: { create: () => Worker; onStart: (worker: ConnectedWorker<Exposed>) => void }) {}

    get current(): ConnectedWorker<Exposed> | undefined {
        return this.#worker;
    }

    start(): void {
        if (this.#worker !== undefined) return;
        this.#worker = new ConnectedWorker(this.options.create());
        this.options.onStart(this.#worker);
    }

    stop(): void {
        this.#worker?.terminate();
        this.#worker = undefined;
    }

    /** Starts a new worker the next time the page is visible. */
    restartOnReturn(): void {
        this.#restartOnReturn = true;
    }

    /** Returns a function that stops following. */
    followPage(): () => void {
        const leave = () => {
            if (this.#worker === undefined) return;
            this.stop();
            this.restartOnReturn();
        };
        const comeBack = () => {
            if (document.hidden || !this.#restartOnReturn) return;
            this.#restartOnReturn = false;
            this.stop();
            this.start();
        };
        addEventListener("pagehide", leave);
        addEventListener("pageshow", comeBack);
        document.addEventListener("visibilitychange", comeBack);
        return () => {
            removeEventListener("pagehide", leave);
            removeEventListener("pageshow", comeBack);
            document.removeEventListener("visibilitychange", comeBack);
        };
    }
}

/**
 * Returns the message of an error that a worker call rejected with.
 */
export function failureMessage(error: unknown): string {
    return error instanceof Error ? error.message : String(error);
}
