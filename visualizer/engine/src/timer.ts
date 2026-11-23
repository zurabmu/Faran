/**
 * Converts elapsed real time into whole steps of `timeStep` seconds. Time that does not fill a
 * whole step yet carries over to the next call.
 */
export class StepTimer {
    readonly #timeStep: number;
    #previousTime: number;
    #timeNotYetStepped = 0;

    /**
     * `startTime` is in milliseconds, on the same clock as the times passed to `stepsDueAt`.
     */
    constructor({ timeStep, startTime }: { timeStep: number; startTime: number }) {
        this.#timeStep = timeStep;
        this.#previousTime = startTime;
    }

    /**
     * Returns how many whole steps have passed between the previous call and `time`, in
     * milliseconds, when time runs at `speed` times real time.
     */
    stepsDueAt(time: number, { speed }: { speed: number }): number {
        this.#timeNotYetStepped += ((time - this.#previousTime) / 1000) * speed;
        this.#previousTime = time;
        const steps = Math.floor(this.#timeNotYetStepped / this.#timeStep);
        this.#timeNotYetStepped -= steps * this.#timeStep;
        return steps;
    }
}
