import { type BlueprintJson, type ViewerRecording, type ViewerState, WebViewer } from "@rerun-io/web-viewer";
import { TIME_TIMELINE } from "@/replay/viewer/clock";

const HIDDEN_PANELS = ["top", "blueprint", "selection", "time"] as const;

/**
 * Starts a Rerun viewer in `parent` that shows only the views of the recording in `contents`.
 */
export async function showRecording({ parent, name, contents }: { parent: HTMLElement; name: string; contents: Uint8Array }): Promise<WebViewer> {
    const viewer = new WebViewer();
    await viewer.start(null, parent, { width: "100%", height: "100%", hideWelcomeScreen: true, theme: "dark" });
    for (const panel of HIDDEN_PANELS) viewer.overridePanelState(panel, "hidden");
    const channel = viewer.openChannel(name);
    channel.sendRrd(contents);
    channel.close();
    return viewer;
}

/**
 * Waits until the viewer has loaded everything and laid out its views.
 */
export async function loadedState(viewer: WebViewer): Promise<ViewerState> {
    for (;;) {
        const state = await viewer.getState();
        if (state.loading.length === 0 && state.views.length > 0) return state;
        await nextFrame();
    }
}

/**
 * The recording the viewer shows. Throws when it shows none.
 */
export function activeRecording(state: ViewerState): ViewerRecording {
    const recording = state.recordings.find((candidate) => candidate.storeId === state.activeStoreId) ?? state.recordings[0];
    if (recording === undefined) throw new Error("Expected the viewer to show a recording, but it has none open.");
    return recording;
}

/**
 * Returns the blueprint with its time panel on `TIME_TIMELINE` at `speed` times real time, and
 * without a play state.
 */
export function withTimePanel(blueprint: BlueprintJson, speed: number): BlueprintJson {
    const { play_state: _, ...panel } = blueprint["/time_panel"]?.["TimePanelBlueprint"] ?? {};
    return { ...blueprint, "/time_panel": { TimePanelBlueprint: { ...panel, timeline: TIME_TIMELINE, playback_speed: speed } } };
}

function nextFrame(): Promise<number> {
    return new Promise((resolve) => requestAnimationFrame(resolve));
}
