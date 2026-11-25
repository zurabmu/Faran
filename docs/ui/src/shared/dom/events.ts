/**
 * Adds `listener` for events of `type` on `target`. Returns a function that removes it.
 */
export function listen<Type extends keyof WindowEventMap>(
    target: Window,
    type: Type,
    listener: (event: WindowEventMap[Type]) => void,
    options: AddEventListenerOptions,
): () => void;
export function listen<Type extends keyof DocumentEventMap>(
    target: Document,
    type: Type,
    listener: (event: DocumentEventMap[Type]) => void,
    options: AddEventListenerOptions,
): () => void;
export function listen<Type extends keyof HTMLElementEventMap>(
    target: HTMLElement,
    type: Type,
    listener: (event: HTMLElementEventMap[Type]) => void,
    options: AddEventListenerOptions,
): () => void;
export function listen(target: EventTarget, type: string, listener: (event: Event) => void, options: AddEventListenerOptions): () => void {
    target.addEventListener(type, listener, options);
    return () => target.removeEventListener(type, listener, options);
}

/**
 * Returns a function that calls each of `stops` once, in reverse order.
 */
export function stopAll(stops: readonly (() => void)[]): () => void {
    return () => {
        for (const stop of [...stops].reverse()) stop();
    };
}
