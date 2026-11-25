import type { FrameClock } from "@engine";

/**
 * Replaces the frames the browser paints in tests. Time stands still and no frame comes until
 * the test shows one.
 */
export class StubFrames implements FrameClock {
    #time = 0;
    #show: ((time: number) => void) | undefined;

    now(): number {
        return this.#time;
    }

    onNextFrame(show: (time: number) => void): () => void {
        this.#show = show;
        return () => {
            this.#show = undefined;
        };
    }

    /**
     * Moves time to `time` and shows the frame that was asked for, if any.
     */
    showFrameAt(time: number): void {
        this.#time = time;
        const show = this.#show;
        this.#show = undefined;
        show?.(time);
    }
}
