import { tick } from "svelte";

/**
 * The element that the address links to, when the page has one.
 */
export function linkedElement(): HTMLElement | undefined {
    return document.getElementById(decodeURIComponent(window.location.hash.slice(1))) ?? undefined;
}

/**
 * Returns the slot of the child of `host` that holds the element the address links to, or an
 * empty string when no child of `host` holds it.
 */
export function linkedSlotIn(host: HTMLElement): string {
    const holder = linkedElement()?.closest<HTMLElement>("[slot]");
    const isChildOfHost = holder?.parentElement === host;
    return isChildOfHost ? holder.slot : "";
}

/**
 * Calls `show` with the slot of the child of `host` that holds the element the address links
 * to, now and whenever the address changes, and scrolls to that element once `show` made it
 * visible. `show` returns whether it showed the slot. Returns a function that stops listening.
 */
export function showLinkedSlots(host: HTMLElement, show: (slot: string) => boolean): () => void {
    const showLinked = async (): Promise<void> => {
        const slot = linkedSlotIn(host);
        if (slot === "" || !show(slot)) return;
        await tick();
        linkedElement()?.scrollIntoView();
    };
    void showLinked();
    const listener = () => void showLinked();
    window.addEventListener("hashchange", listener);
    return () => window.removeEventListener("hashchange", listener);
}
