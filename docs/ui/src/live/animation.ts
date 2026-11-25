import type { Animation } from "@engine";
import type { AnimationPlayer } from "@/shared/player";

/**
 * Mounts `animation` in `element` with the canvas engine, which it loads on first use, and lets
 * `player` drive it. Returns a function that disconnects the player and removes the animation.
 */
export function mountPlayed({ element, animation, player }: { element: HTMLElement; animation: Animation; player: AnimationPlayer }): () => void {
    const mounted = import("@engine").then(({ mountAnimation }) => {
        const mount = mountAnimation(element, animation, { autoplay: true, controls: false });
        return { mount, disconnect: player.connect(mount.playback) };
    });
    return () =>
        void mounted.then(({ mount, disconnect }) => {
            disconnect();
            mount.destroy();
        });
}
