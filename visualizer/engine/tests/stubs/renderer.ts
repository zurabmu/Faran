import type { Camera, Object3D } from "three";
import type { SceneRenderer } from "@faran/engine";

/**
 * Records what a scene canvas asks its renderer to do, on a canvas whose size on screen the test
 * sets and changes.
 */
export class StubRenderer implements SceneRenderer {
    readonly renders: { scene: Object3D; camera: Camera }[] = [];
    fittedSize = { width: 0, height: 0 };

    constructor(readonly canvas: { clientWidth: number; clientHeight: number }) {}

    fitDrawingTo(size: { width: number; height: number }): void {
        this.fittedSize = size;
    }

    render(scene: Object3D, camera: Camera): void {
        this.renders.push({ scene, camera });
    }

    dispose(): void {}
}
