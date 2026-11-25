import { flushSync } from "svelte";
import type { Attachment } from "svelte/attachments";
import { prefersReducedMotion } from "svelte/motion";

/**
 * Grows an element to fill the browser window as a popover and shrinks it back. While the
 * element is expanded, `reservedHeight` keeps its place in the page, and the page does not
 * scroll. `attach` connects the element.
 */
export class Expansion {
    expanded = $state(false);
    transitioning = $state(false);
    reservedHeight = $state("auto");

    #element: HTMLElement | undefined;
    #unlockScroll: () => void = () => {};

    readonly attach: Attachment<HTMLElement> = (element) => {
        this.#element = element;
        return () => {
            if (this.expanded) this.#shrink(element);
            this.#element = undefined;
        };
    };

    toggle(): void {
        const element = this.#connected();
        this.#changeVisibly(() => (this.expanded ? this.#shrink(element) : this.#grow(element)));
    }

    shrinkOnEscape(event: KeyboardEvent): void {
        const shouldShrink = event.key === "Escape" && this.expanded;
        if (shouldShrink) this.toggle();
    }

    #changeVisibly(change: () => void): void {
        const canAnimate = !prefersReducedMotion.current && "startViewTransition" in document;
        if (!canAnimate) return change();
        this.transitioning = true;
        flushSync();
        void document.startViewTransition(change).finished.finally(() => (this.transitioning = false));
    }

    #grow(element: HTMLElement): void {
        this.reservedHeight = `${element.offsetHeight}px`;
        this.expanded = true;
        flushSync();
        element.showPopover();
        this.#unlockScroll = lockPageScroll();
    }

    #shrink(element: HTMLElement): void {
        element.hidePopover();
        this.expanded = false;
        this.reservedHeight = "auto";
        flushSync();
        this.#unlockScroll();
    }

    #connected(): HTMLElement {
        if (this.#element === undefined) throw new Error("Expected the expansion to be attached to an element, but it is not.");
        return this.#element;
    }
}

function lockPageScroll(): () => void {
    const root = document.documentElement.style;
    root.overflow = "hidden";
    return () => root.removeProperty("overflow");
}
