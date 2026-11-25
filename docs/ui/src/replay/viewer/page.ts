const VISUALIZATION_PARAMETER = "visualization";

/**
 * The path of the `.frn` file that the address of the replay page asks for, relative to the
 * page, or an empty string when it asks for none.
 */
export function requestedVisualization(): string {
    return new URLSearchParams(window.location.search).get(VISUALIZATION_PARAMETER) ?? "";
}

/**
 * Tells the reader in `parent` how to ask the replay page for a visualization.
 */
export function showUsage(parent: HTMLElement): void {
    const message = document.createElement("p");
    message.id = "message";
    message.textContent = `Add ?${VISUALIZATION_PARAMETER}=<path to .frn file> to the address.`;
    parent.replaceChildren(message);
}

/**
 * Downloads the recording at `visualization`, relative to the replay page. Throws when the
 * server does not return it.
 */
export async function fetchRecording(visualization: string): Promise<Uint8Array> {
    const response = await fetch(new URL(visualization, window.location.href));
    if (!response.ok) throw new Error(`Expected the replay ${visualization} to load, but the server answered ${response.status}.`);
    return new Uint8Array(await response.arrayBuffer());
}
