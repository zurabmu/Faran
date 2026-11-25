import type { SizeWatcher } from "@faran/engine";

/**
 * A size watcher that reports a resize when the test calls `resize`.
 */
export class StubSizeWatcher {
    #onResize: () => void = () => {};

    readonly watch: SizeWatcher = (onResize) => {
        this.#onResize = onResize;
        return () => {
            this.#onResize = () => {};
        };
    };

    resize(): void {
        this.#onResize();
    }
}
