import { mount, unmount } from "svelte";
import type { Animation } from "@engine/animation";
import { Playback } from "@engine/playback.svelte";
import Player from "@engine/player/Player.svelte";

const OPEN_LEGEND_MINIMUM_WIDTH = 560;

/**
 * A mounted animation player.
 */
export interface MountedAnimation {
    readonly playback: Playback;
    destroy(): void;
}

/**
 * Mounts an animation player in `container`. If `controls` is `false`, the
 * caller controls the playback.
 */
export function mountAnimation(
    container: HTMLElement,
    animation: Animation,
    { autoplay, controls }: { autoplay: boolean; controls: boolean },
): MountedAnimation {
    const playback = new Playback({ stepCount: animation.frames.length, timeStep: animation.timeStep });
    const isPlayable = animation.frames.length > 1;
    const isWide = container.clientWidth >= OPEN_LEGEND_MINIMUM_WIDTH;
    const player = mount(Player, {
        target: container,
        props: { animation, playback, showsControls: isPlayable && controls, legendOpen: isWide },
    });
    const startsPlaying = autoplay && isPlayable;
    if (startsPlaying) playback.play();
    return {
        playback,
        destroy() {
            playback.pause();
            void unmount(player);
        },
    };
}
