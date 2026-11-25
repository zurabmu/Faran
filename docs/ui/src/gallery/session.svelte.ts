import type { Attachment } from "svelte/attachments";
import { cubicInOut } from "svelte/easing";
import { prefersReducedMotion, Tween } from "svelte/motion";
import { listen, stopAll } from "@/shared/dom/events";
import { Timeout } from "@/shared/timeout";

const ADVANCE_INTERVAL = 8000;
const WASH_DURATION = 900;
const NOT_CHANGING = -1;
const AWAY_SPEED = 1.4;
const FORMING_SPEED = 1.25;
const BLUR_PER_WASH = 2;

/**
 * Which section of a gallery is shown, and the change between sections. It advances to the
 * next section on its own while the reader does not engage with it, and calls `onChange` on
 * every change.
 */
export class GallerySession {
    shown = $state(0);
    outgoing = $state(NOT_CHANGING);
    #held = false;
    readonly #advance = new Timeout();
    readonly #wash = new Tween(0, { duration: WASH_DURATION, easing: cubicInOut });

    constructor(
        private readonly count: number,
        private readonly onChange: () => void,
    ) {}

    /**
     * How far the outgoing section has washed away, from 0 to 1.
     */
    get away(): number {
        return this.#isChanging ? Math.min(1, this.#wash.current * AWAY_SPEED) : 0;
    }

    /**
     * How much of the shown section is still forming, from 1 at the start of a change to 0.
     */
    get forming(): number {
        return this.#isChanging ? Math.max(0, 1 - this.#wash.current * FORMING_SPEED) : 0;
    }

    /**
     * Whether the section at `index` takes part in the page: the shown one and the outgoing one.
     */
    isVisible(index: number): boolean {
        return index === this.shown || index === this.outgoing;
    }

    /**
     * How washed out the section at `index` is, from 0 to 1.
     */
    washOf(index: number): number {
        if (index === this.shown) return this.forming;
        if (index === this.outgoing) return this.away;
        return 0;
    }

    /**
     * The CSS filter that washes out the section at `index`, through the SVG filter that
     * `WashFilters` defines for it.
     */
    filterOf(index: number): string {
        const amount = this.washOf(index);
        const filter = index === this.shown ? "wash-forming" : "wash-away";
        return amount === 0 ? "" : `url(#${filter}) blur(${amount * BLUR_PER_WASH}px)`;
    }

    /**
     * Starts advancing on its own. Returns a function that stops it.
     */
    start(): () => void {
        this.#schedule();
        return () => this.#advance.cancel();
    }

    /**
     * Holds the shown section while the pointer is over the element or the focus is inside it.
     */
    readonly holdWhileEngaged: Attachment<HTMLElement> = (element) => {
        const hold = () => (this.#held = true);
        const release = () => requestAnimationFrame(() => (this.#held = isEngaged(element)));
        return stopAll([
            listen(element, "pointerenter", hold, {}),
            listen(element, "focusin", hold, {}),
            listen(element, "pointerleave", release, {}),
            listen(element, "focusout", release, {}),
        ]);
    };

    show(index: number): void {
        const canChange = index !== this.shown && !this.#isChanging;
        if (!canChange) return;
        this.#schedule();
        const outgoing = this.shown;
        this.shown = index;
        this.onChange();
        if (!prefersReducedMotion.current) void this.#washAway(outgoing);
    }

    #schedule(): void {
        this.#advance.cancel();
        if (!prefersReducedMotion.current) this.#advance.start(ADVANCE_INTERVAL, () => this.#advanceUnlessHeld());
    }

    #advanceUnlessHeld(): void {
        const isWatched = this.#held || document.hidden;
        if (isWatched) this.#schedule();
        else this.show((this.shown + 1) % this.count);
    }

    get #isChanging(): boolean {
        return this.outgoing !== NOT_CHANGING;
    }

    async #washAway(outgoing: number): Promise<void> {
        this.outgoing = outgoing;
        await this.#wash.set(0, { duration: 0 });
        await this.#wash.set(1);
        this.outgoing = NOT_CHANGING;
    }
}

function isEngaged(element: HTMLElement): boolean {
    return element.matches(":hover") || element.matches(":focus-within");
}
