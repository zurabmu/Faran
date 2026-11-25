import type { PlayerControls } from "@/shared/player";
import { releaseProxy } from "comlink";
import { connectToReplay, type ReplayCommands, type ReplayReport } from "@/replay/messages";

const DISCONNECTED: ReplayCommands = {
    play: notConnected,
    pause: notConnected,
    seek: notConnected,
    changeSpeed: notConnected,
    resetLayout: notConnected,
};

/**
 * Controls a Rerun replay in the replay page `docs/content/viewer/index.html`, loaded in an
 * iframe. It is ready once the replay page reports its first state.
 */
export class ReplayPlayer implements PlayerControls {
    ready = $state(false);
    playing = $state(false);
    step = $state(0);
    first = $state(0);
    last = $state(0);
    seconds = $state(0);
    endSeconds = $state(0);
    speed = $state(1);

    #replay: ReplayCommands = DISCONNECTED;

    /**
     * Connects to the replay page in `frame`. Returns a function that disconnects it.
     */
    connect(frame: HTMLIFrameElement): () => void {
        const replay = connectToReplay({ frame, receive: (report) => this.#mirror(report) });
        this.#replay = replay;
        return () => {
            replay[releaseProxy]();
            this.#replay = DISCONNECTED;
        };
    }

    toggle(): void {
        void (this.playing ? this.#replay.pause() : this.#replay.play());
    }

    seek(step: number): void {
        this.step = Math.min(Math.max(step, this.first), this.last);
        void this.#replay.seek(this.step);
    }

    stepBy(count: number): void {
        this.seek(this.step + count);
    }

    changeSpeed(speed: number): void {
        this.speed = speed;
        void this.#replay.changeSpeed(speed);
    }

    resetLayout(): void {
        void this.#replay.resetLayout();
    }

    #mirror(report: ReplayReport): void {
        this.ready = true;
        this.playing = report.playing;
        this.step = report.step;
        this.first = report.first;
        this.last = report.last;
        this.seconds = report.seconds;
        this.endSeconds = report.endSeconds;
    }
}

function notConnected(): Promise<void> {
    throw new Error("The replay player is not connected to a replay frame.");
}
