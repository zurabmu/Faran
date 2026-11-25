import type { Animation } from "@engine";
import { proxy } from "comlink";
import { pythonAssetsUrl } from "@/shared/site";
import { ConnectedWorker } from "@/shared/worker";
import type { SnippetWorker } from "@/live/worker";

/**
 * Runs snippets one at a time, in the order they were requested.
 */
class SnippetRunner {
    #worker: ConnectedWorker<SnippetWorker> | undefined;

    /**
     * Runs `source` and returns the animation it saved. Calls `report` with what the worker is doing.
     */
    run(source: string, report: (text: string) => void): Promise<Animation> {
        this.#worker ??= new ConnectedWorker(new Worker(new URL("./worker.ts", import.meta.url), { type: "module" }));
        const snippet = { source, assetsUrl: pythonAssetsUrl() };
        return this.#worker.call((worker) => worker.run(snippet, proxy(report)));
    }
}

export const snippetRunner = new SnippetRunner();
