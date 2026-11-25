import type { Animation } from "@engine";
import { FIRST_RUN_DOWNLOADS } from "@/shared/python";
import { failureMessage } from "@/shared/worker";
import type { SnippetEditor } from "@/live/editor";
import { snippetRunner } from "@/live/runner";

/**
 * The state of one live snippet: its editor, whether it runs, what the run reports, and the
 * animation of the latest successful run.
 */
export class LiveSession {
    running = $state(false);
    status = $state(`Runs in your browser. ${FIRST_RUN_DOWNLOADS}`);
    failure = $state("");
    animation = $state.raw<Animation | undefined>(undefined);
    editable = $state(false);
    #editor: SnippetEditor;

    constructor(private readonly source: string) {
        this.#editor = uneditable(source);
    }

    /**
     * Creates the editor inside `element`, which it loads on first use. Returns a function that
     * removes it.
     */
    attachEditor(element: HTMLElement): () => void {
        const created = import("@/live/editor").then(({ createEditor }) => this.#useEditor(createEditor({ parent: element, source: this.source })));
        return () => void created.then((editor) => editor.destroy());
    }

    run(): void {
        this.running = true;
        this.failure = "";
        this.status = "Starting";
        snippetRunner.run(this.#editor.source, (text) => (this.status = text)).then(
            (animation) => this.#show(animation),
            (error: unknown) => this.#fail(failureMessage(error)),
        );
    }

    reset(): void {
        this.#editor.reset();
    }

    #useEditor(editor: SnippetEditor): SnippetEditor {
        this.#editor = editor;
        this.editable = true;
        return editor;
    }

    #show(animation: Animation): void {
        this.animation = animation;
        this.running = false;
        this.status = "Done";
    }

    #fail(message: string): void {
        this.failure = message;
        this.running = false;
        this.status = "Failed";
    }
}

function uneditable(source: string): SnippetEditor {
    return { source, reset: () => {}, destroy: () => {} };
}
