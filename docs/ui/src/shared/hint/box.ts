export type HintPlacement = "above" | "below";

export type HintAlignment = "start" | "end";

/**
 * Where a hint sits, in CSS pixels from the top left corner of its container, and on which
 * side of its target the popup opens.
 */
export interface HintBox {
    readonly left: number;
    readonly top: number;
    readonly width: number;
    readonly height: number;
    readonly placement: HintPlacement;
    readonly alignment: HintAlignment;
}

/**
 * Returns the box around `target` inside `container`. The popup opens towards the larger part
 * of the container.
 */
export function boxAround({ target, container }: { target: HTMLElement; container: HTMLElement }): HintBox {
    const rect = target.getBoundingClientRect();
    const bounds = container.getBoundingClientRect();
    const left = rect.left - bounds.left;
    const top = rect.top - bounds.top;
    const isInUpperHalf = top + rect.height / 2 < bounds.height / 2;
    const isInLeftHalf = left + rect.width / 2 < bounds.width / 2;
    return {
        left,
        top,
        width: rect.width,
        height: rect.height,
        placement: isInUpperHalf ? "below" : "above",
        alignment: isInLeftHalf ? "start" : "end",
    };
}
