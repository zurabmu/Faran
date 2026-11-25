/**
 * One pending timeout at a time. Starting a new one cancels the pending one.
 */
export class Timeout {
    #timer = 0;

    get pending(): boolean {
        return this.#timer !== 0;
    }

    start(milliseconds: number, callback: () => void): void {
        this.cancel();
        this.#timer = window.setTimeout(() => {
            this.#timer = 0;
            callback();
        }, milliseconds);
    }

    cancel(): void {
        window.clearTimeout(this.#timer);
        this.#timer = 0;
    }
}
