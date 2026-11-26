import { cubicOut } from "svelte/easing";
import { Tween } from "svelte/motion";
import { Timeout } from "@/shared/timeout";

const DELAY = 100;
const DROP_LEAD = 150;
const DURATION = 1800;

/**
 * How far an element has surfaced since it came fully into view, from 0 to 1. Calls `onRipple`
 * shortly before it starts to rise.
 */
export class Surfacing {
    readonly #progress = new Tween(0, { duration: DURATION, easing: cubicOut });
    readonly #rising = new Timeout();

    constructor(private readonly onRipple: (element: Element) => void) {}

    get progress(): number {
        return this.#progress.current;
    }

    watch(element: Element): () => void {
        const observer = new IntersectionObserver(
            ([entry]) => {
                if (entry === undefined) return;
                if (entry.intersectionRatio >= 0.99) this.#riseSoon(element);
                else if (!entry.isIntersecting) this.#sink();
            },
            { threshold: [0, 0.99] },
        );
        observer.observe(element);
        return () => {
            observer.disconnect();
            this.#sink();
        };
    }

    #riseSoon(element: Element): void {
        const isRising = this.#progress.target > 0 || this.#rising.pending;
        if (isRising) return;
        this.#rising.start(DELAY, () => this.#rise(element));
    }

    #rise(element: Element): void {
        this.onRipple(element);
        this.#rising.start(DROP_LEAD, () => void this.#progress.set(1));
    }

    #sink(): void {
        this.#rising.cancel();
        void this.#progress.set(0, { duration: 0 });
    }
}
