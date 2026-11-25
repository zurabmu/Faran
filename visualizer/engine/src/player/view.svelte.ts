import type { Animation, Frame, Rendering } from "@/animation";
import type { Playback } from "@/playback.svelte";
import { type Bounds, boundsOf } from "@/view";

/**
 * What the player shows of an animation at the playback's step.
 */
export class PlayerView {
    readonly frame: Frame;
    readonly bounds: Bounds;
    readonly hasSidePanel: boolean;

    constructor(shown: () => { readonly animation: Animation; readonly playback: Playback }) {
        this.frame = $derived(frameAt(shown().animation, shown().playback.step));
        this.bounds = $derived(boundsOf(everyRenderingOf(shown().animation)));
        this.hasSidePanel = $derived(hasInfoOrCharts(shown().animation));
    }
}

function frameAt(animation: Animation, step: number): Frame {
    const frame = animation.frames[step];
    if (frame === undefined) throw new Error(`Expected the animation to have a frame at step ${step}, but it has ${animation.frames.length} frames.`);
    return frame;
}

function hasInfoOrCharts(animation: Animation): boolean {
    return animation.charts.length > 0 || animation.frames.some((frame) => frame.info.length > 0);
}

function everyRenderingOf(animation: Animation): Rendering[] {
    return [...animation.background, ...animation.frames.flatMap((frame) => frame.renderings)];
}
