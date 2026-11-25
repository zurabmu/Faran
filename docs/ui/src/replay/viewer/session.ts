import type { BlueprintJson, WebViewer } from "@rerun-io/web-viewer";
import type { ReplayPage, ReplayReport } from "@/replay/messages";
import { type ReplayClock, readClock, TIME_TIMELINE } from "@/replay/viewer/clock";
import { activeRecording, loadedState, withTimePanel } from "@/replay/viewer/rerun";

/**
 * Plays a recording for the page that embeds this one, and reports the position and play state
 * after every change.
 */
export class ReplaySession implements ReplayPage {
    #clock: ReplayClock;
    #speed = 1;
    #reportScheduled = false;
    #receive: (report: ReplayReport) => void = () => undefined;

    private constructor(
        private readonly viewer: WebViewer,
        private readonly layout: BlueprintJson,
        clock: ReplayClock,
    ) {
        this.#clock = clock;
    }

    /**
     * Waits until the viewer has loaded its recording and remembers the recording's layout.
     */
    static async open(viewer: WebViewer): Promise<ReplaySession> {
        const state = await loadedState(viewer);
        const { blueprint } = await viewer.getBlueprint({ kind: "recording" });
        return new ReplaySession(viewer, blueprint, readClock(activeRecording(state)));
    }

    /**
     * Starts playing from the first step.
     */
    async start(): Promise<void> {
        const scheduleReport = () => this.#scheduleReport();
        this.viewer.on("time_update", scheduleReport);
        this.viewer.on("timeline_change", scheduleReport);
        this.viewer.on("play", scheduleReport);
        this.viewer.on("pause", scheduleReport);
        await this.resetLayout();
        await this.#playFrom(this.#clock.first);
    }

    subscribe(receive: (report: ReplayReport) => void): void {
        this.#receive = receive;
        this.#scheduleReport();
    }

    async play(): Promise<void> {
        if (this.#clock.atEnd) await this.#playFrom(this.#clock.first);
        else await this.viewer.setTime({ timeline: TIME_TIMELINE, playState: "playing" });
        this.#scheduleReport();
    }

    async pause(): Promise<void> {
        await this.#pauseViewer();
        this.#scheduleReport();
    }

    async seek(step: number): Promise<void> {
        await this.viewer.setTime({ timeline: TIME_TIMELINE, durationNanos: this.#clock.timeAt(Math.round(step)), playState: "paused" });
        this.#scheduleReport();
    }

    async changeSpeed(speed: number): Promise<void> {
        this.#speed = speed;
        const { blueprint } = await this.viewer.getBlueprint({ kind: "recording" });
        await this.viewer.setBlueprint(withTimePanel(blueprint, speed), { kind: "recording" });
    }

    async resetLayout(): Promise<void> {
        await this.viewer.setBlueprint(withTimePanel(this.layout, this.#speed), { kind: "recording" });
    }

    async #playFrom(step: number): Promise<void> {
        await this.viewer.setTime({ timeline: TIME_TIMELINE, durationNanos: this.#clock.timeAt(step), playState: "playing" });
        this.#scheduleReport();
    }

    async #pauseViewer(): Promise<void> {
        await this.viewer.setTime({ timeline: TIME_TIMELINE, playState: "paused" });
    }

    #scheduleReport(): void {
        if (this.#reportScheduled) return;
        this.#reportScheduled = true;
        requestAnimationFrame(() => void this.#report());
    }

    async #report(): Promise<void> {
        this.#reportScheduled = false;
        const recording = activeRecording(await this.viewer.getState());
        this.#clock = readClock(recording);
        const playing = recording.playState === "playing";
        const playedPastEnd = playing && this.#clock.atEnd;
        if (playedPastEnd) await this.#pauseViewer();
        this.#receive(reportOf(this.#clock, { playing: playing && !playedPastEnd }));
    }
}

function reportOf({ first, last, step, seconds, endSeconds }: ReplayClock, { playing }: { playing: boolean }): ReplayReport {
    return { first, last, step, seconds, endSeconds, playing };
}
