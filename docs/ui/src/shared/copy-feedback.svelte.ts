import { copyText } from "@/shared/clipboard";
import { Timeout } from "@/shared/timeout";

type CopyState = "idle" | "copied" | "refused";

const SHOWN_MILLISECONDS = 2200;

/**
 * Copies text and keeps the result visible for a short time, so a button can
 * show "Copied" or tell the reader to copy by hand.
 */
export class CopyFeedback {
    state = $state<CopyState>("idle");
    readonly #reset = new Timeout();

    async copy(text: string): Promise<void> {
        this.state = (await copyText(text)) ? "copied" : "refused";
        this.#reset.start(SHOWN_MILLISECONDS, () => (this.state = "idle"));
    }
}
