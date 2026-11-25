/**
 * Calls `onResize` whenever an element changes its size on screen, until the returned function is
 * called.
 */
export type SizeWatcher = (onResize: () => void) => () => void;

/**
 * Watches the size of `element` on screen.
 */
export function sizeWatcherOf(element: Element): SizeWatcher {
    return (onResize) => {
        const resizes = new ResizeObserver(onResize);
        resizes.observe(element);
        return () => resizes.disconnect();
    };
}
