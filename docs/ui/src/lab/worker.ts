import type { Frame } from "@engine";
import { expose } from "comlink";
import { LatestCall } from "@/shared/latest";
import { labExport } from "@/shared/python";
import { wait } from "@/shared/wait";
import type { LabReceiver, LabStep } from "@/lab/messages";

interface Simulation {
    background(): string;
    advance(): string;
    destroy(): void;
}

interface Demos {
    get(name: string): () => Simulation;
}

const loadDemos = labExport<Demos>("demos");
const runs = new LatestCall();

const labWorker = {
    /**
     * Runs a demo until it finishes or another run or `stop` replaces it, and sends its
     * background and steps to `receiver`.
     *
     * @param demo Key of the `demos` mapping in `docs/lab/scenarios.py`.
     */
    async run({ demo, assetsUrl }: { demo: string; assetsUrl: string }, receiver: LabReceiver): Promise<void> {
        const isLatest = runs.begin();
        const demos = await loadDemos({ assetsUrl, report: (text) => receiver.onStatus(text) });
        if (!isLatest()) return;
        receiver.onStatus("Planning");
        await play(demos.get(demo)(), { receiver, isLatest });
    },

    /**
     * Stops the running demo after its current planner step.
     */
    stop(): void {
        runs.cancel();
    },
};

/**
 * The demo runner that `lab/worker.ts` exposes.
 */
export type LabWorker = typeof labWorker;

expose(labWorker);

async function play(simulation: Simulation, { receiver, isLatest }: { receiver: LabReceiver; isLatest: () => boolean }): Promise<void> {
    receiver.onBackground(backgroundOf(simulation));
    let finished = false;
    while (!finished && isLatest()) {
        const step = advance(simulation);
        receiver.onStep(step);
        finished = step.finished;
        await wait(0);
    }
    simulation.destroy();
}

function backgroundOf(simulation: Simulation): Frame {
    return JSON.parse(simulation.background()) as Frame;
}

function advance(simulation: Simulation): LabStep {
    return JSON.parse(simulation.advance()) as LabStep;
}
