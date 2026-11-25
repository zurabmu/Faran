/**
 * Calls `onVisible` once, the first time `element` intersects the viewport as `options` define
 * it. Returns a function that stops watching.
 */
export function whenVisible(element: Element, options: IntersectionObserverInit, onVisible: () => void): () => void {
    const observer = new IntersectionObserver((entries) => {
        const isVisible = entries.some((entry) => entry.isIntersecting);
        if (!isVisible) return;
        observer.disconnect();
        onVisible();
    }, options);
    observer.observe(element);
    return () => observer.disconnect();
}

/**
 * Calls `onResize` whenever `element` changes size. Returns a function that stops watching.
 */
export function whenResized(element: Element, onResize: () => void): () => void {
    const observer = new ResizeObserver(onResize);
    observer.observe(element);
    return () => observer.disconnect();
}
