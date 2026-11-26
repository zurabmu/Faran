const LOADED_ATTRIBUTE = "data-faran-loaded";

/**
 * Marks the page as loaded on the next animation frame, after the components have rendered. The
 * stylesheets keep the page content hidden until then.
 */
export function markPageLoaded(): void {
    requestAnimationFrame(() => document.documentElement.setAttribute(LOADED_ATTRIBUTE, ""));
}
