/**
 * Tells whether `name` was marked in this browser with `markFlag`.
 * Returns false when the browser blocks storage.
 */
export function hasFlag(name: string): boolean {
    try {
        return window.localStorage.getItem(flagKey(name)) !== null;
    } catch {
        return false;
    }
}

/**
 * Marks `name` in this browser, so `hasFlag` returns true on later page loads.
 * Does nothing when the browser blocks storage.
 */
export function markFlag(name: string): void {
    try {
        window.localStorage.setItem(flagKey(name), "1");
    } catch {
        return;
    }
}

function flagKey(name: string): string {
    return `faran:${name}`;
}
