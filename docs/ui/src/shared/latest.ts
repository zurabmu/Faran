/**
 * Tells which of several overlapping calls is the latest, so that an earlier call can stop
 * once a later one starts.
 */
export class LatestCall {
    #count = 0;

    /**
     * Starts a call and returns a function that tells whether it is still the latest.
     */
    begin(): () => boolean {
        this.#count += 1;
        const call = this.#count;
        return () => call === this.#count;
    }

    /**
     * Makes every call that has begun no longer the latest.
     */
    cancel(): void {
        this.#count += 1;
    }
}
