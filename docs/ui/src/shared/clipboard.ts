/**
 * Copies text to the clipboard and reports whether the browser allowed it.
 * Pages served without HTTPS, and some embedded views, refuse clipboard access.
 */
export async function copyText(text: string): Promise<boolean> {
    try {
        await navigator.clipboard.writeText(text);
        return true;
    } catch {
        return false;
    }
}
