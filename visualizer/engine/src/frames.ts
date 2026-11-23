/**
 * Tells playback the current time and when the screen shows its next frame, both in
 * milliseconds.
 */
export interface FrameClock {
    now(): number;

    /**
     * Calls `show` with the time of the next frame. Returns a function that cancels the call.
     */
    onNextFrame(show: (time: number) => void): () => void;
}

/**
 * The frames the browser paints on screen.
 */
export const screenFrames: FrameClock = {
    now: () => performance.now(),
    onNextFrame(show) {
        const frame = requestAnimationFrame(show);
        return () => cancelAnimationFrame(frame);
    },
};
