import type { ViewerRecording, ViewerTimeline } from "@rerun-io/web-viewer";

/**
 * The timeline that the replay plays on, in nanoseconds of simulation time.
 */
export const TIME_TIMELINE = "time";

const STEP_TIMELINE = "step";
const NANOSECONDS_PER_SECOND = 1e9;

/**
 * Where a recording's time cursor is, as a simulation step and in seconds.
 */
export interface ReplayClock {
    readonly first: number;
    readonly last: number;
    readonly step: number;
    readonly seconds: number;
    readonly endSeconds: number;
    readonly atEnd: boolean;

    /**
     * The time in nanoseconds on `TIME_TIMELINE` of `step`, clamped to the recorded steps.
     */
    timeAt(step: number): number;
}

/**
 * Reads the clock of a recording that the Faran visualizer wrote. Throws when the recording has
 * no data on its step or time timeline.
 */
export function readClock(recording: ViewerRecording): ReplayClock {
    const steps = rangeOf(recording, STEP_TIMELINE);
    const times = timelineOf(recording, TIME_TIMELINE);
    const timeRange = rangeOf(recording, TIME_TIMELINE);
    const first = Number(steps.start);
    const last = Number(steps.end);
    const start = Number(timeRange.start);
    const end = Number(timeRange.end);
    const timeStep = last > first ? (end - start) / (last - first) : 0;
    const time = Number(times.currentTime ?? timeRange.start);
    return {
        first,
        last,
        step: timeStep === 0 ? first : first + Math.round((time - start) / timeStep),
        seconds: time / NANOSECONDS_PER_SECOND,
        endSeconds: end / NANOSECONDS_PER_SECOND,
        atEnd: time >= end,
        timeAt: (step) => Math.round(start + (Math.min(Math.max(step, first), last) - first) * timeStep),
    };
}

function timelineOf(recording: ViewerRecording, name: string): ViewerTimeline {
    const timeline = recording.timelines.find((candidate) => candidate.name === name);
    if (timeline === undefined) throw new Error(`The recording ${recording.storeId} has no "${name}" timeline.`);
    return timeline;
}

function rangeOf(recording: ViewerRecording, name: string): { start: bigint; end: bigint } {
    const range = timelineOf(recording, name).timeRange;
    if (range === undefined) throw new Error(`The "${name}" timeline of the recording ${recording.storeId} has no data.`);
    return range;
}
