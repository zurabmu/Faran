import type { Attachment } from "svelte/attachments";
import { listen, stopAll } from "@/shared/dom/events";
import { whenResized, whenVisible } from "@/shared/dom/visibility";
import { hasFlag, markFlag } from "@/shared/storage";
import { Timeout } from "@/shared/timeout";
import { type HintBox, boxAround } from "@/shared/hint/box";

const STEP_MILLISECONDS = 3200;
const VISIBLE_SHARE = 0.6;

/**
 * Points at a sequence of buttons, one at a time. It plays once per browser for each `name`. The
 * container must be positioned and hold every target.
 */
export class HintTour {
    index = $state(0);
    visible = $state(false);
    box = $state<HintBox>({ left: 0, top: 0, width: 0, height: 0, placement: "below", alignment: "start" });

    readonly #name: string;
    readonly #texts: string[];
    readonly #targets: HTMLElement[] = [];
    readonly #nextStep = new Timeout();

    constructor({ name, texts }: { name: string; texts: string[] }) {
        this.#name = name;
        this.#texts = texts;
    }

    get text(): string {
        return itemAt(this.#texts, this.index, "hint text");
    }

    /**
     * Returns an attachment that makes its element the target of the text at `index`.
     */
    target(index: number): Attachment<HTMLElement> {
        return (element) => {
            this.#targets[index] = element;
        };
    }

    /**
     * Plays the tour once `container` is mostly in view, unless this browser has played it
     * before. Returns a function that stops the tour and removes the listeners.
     */
    connect(container: HTMLElement): () => void {
        return stopAll([
            whenVisible(container, { threshold: VISIBLE_SHARE }, () => this.#playOnce(container)),
            whenResized(container, () => this.#followResize(container)),
            listen(container, "pointerdown", () => this.#stop(), {}),
            listen(container, "keydown", () => this.#stop(), {}),
            () => this.#stop(),
        ]);
    }

    #playOnce(container: HTMLElement): void {
        if (hasFlag(this.#name)) return;
        markFlag(this.#name);
        this.#showStep(container, 0);
    }

    #showStep(container: HTMLElement, index: number): void {
        this.index = index;
        this.visible = true;
        this.#measure(container);
        this.#nextStep.start(STEP_MILLISECONDS, () => this.#advance(container));
    }

    #advance(container: HTMLElement): void {
        const hasNextStep = this.index + 1 < this.#texts.length;
        if (hasNextStep) this.#showStep(container, this.index + 1);
        else this.#stop();
    }

    #followResize(container: HTMLElement): void {
        if (this.visible) this.#measure(container);
    }

    #measure(container: HTMLElement): void {
        this.box = boxAround({ target: itemAt(this.#targets, this.index, "hint target"), container });
    }

    #stop(): void {
        this.#nextStep.cancel();
        this.visible = false;
    }
}

function itemAt<T>(items: readonly T[], index: number, description: string): T {
    const item = items[index];
    if (item === undefined) throw new Error(`Expected a ${description} at index ${index}, found ${items.length} of them.`);
    return item;
}
