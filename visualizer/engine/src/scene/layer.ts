import type { Group } from "three";
import type { Rendering } from "@engine/animation";
import type { CameraBox } from "@engine/view";

/**
 * The area of the scene a draw shows, and the canvas size in CSS pixels.
 */
export interface Viewport {
    readonly box: CameraBox;
    readonly width: number;
    readonly height: number;
}

/**
 * The three.js objects that show one rendering, updated in place between draws.
 */
export interface Layer {
    /**
     * A group that holds the objects of the layer, so that its render order orders all of them.
     */
    readonly object: Group;

    /**
     * Shows the rendering and returns true, or returns false without a change when the rendering
     * is of a kind this layer cannot show.
     */
    show(rendering: Rendering, viewport: Viewport): boolean;

    /**
     * Releases the GPU resources of the layer.
     */
    dispose(): void;
}
