import type { Animation } from "@engine";
import { expose } from "comlink";
import { labExport } from "@/shared/python";

type RunSnippet = (source: string) => Promise<string>;

const loadRunSnippet = labExport<RunSnippet>("run_snippet");
let queue: Promise<unknown> = Promise.resolve();

const snippetWorker = {
    /**
     * Runs a snippet after the ones requested before it and returns the animation it saved.
     * `report` receives status texts.
     */
    run({ source, assetsUrl }: { source: string; assetsUrl: string }, report: (text: string) => void): Promise<Animation> {
        const animation = queue.then(() => runInTurn({ source, assetsUrl }, report));
        queue = animation.catch(() => undefined);
        return animation;
    },
};

/**
 * The snippet runner that `live/worker.ts` exposes with Comlink.
 */
export type SnippetWorker = typeof snippetWorker;

expose(snippetWorker);

async function runInTurn({ source, assetsUrl }: { source: string; assetsUrl: string }, report: (text: string) => void): Promise<Animation> {
    const runSnippet = await loadRunSnippet({ assetsUrl, report });
    report("Running");
    return JSON.parse(await runSnippet(source)) as Animation;
}
