const DROP_EVENT = "faran:water-drop";

/**
 * A drop at a point of the viewport, in CSS pixels. A strength of 1 is a click.
 */
export interface Drop {
    readonly x: number;
    readonly y: number;
    readonly strength: number;
}

/**
 * Lets a drop fall on the water surface behind the page, if the page has one and the reader
 * does not prefer reduced motion.
 */
export function dropOnWater(drop: Drop): void {
    window.dispatchEvent(new CustomEvent<Drop>(DROP_EVENT, { detail: drop }));
}

/**
 * Calls `receive` for every drop that `dropOnWater` lets fall. Returns a function that stops listening.
 */
export function listenForDrops(receive: (drop: Drop) => void): () => void {
    const listener = (event: Event) => receive((event as CustomEvent<Drop>).detail);
    window.addEventListener(DROP_EVENT, listener);
    return () => window.removeEventListener(DROP_EVENT, listener);
}
