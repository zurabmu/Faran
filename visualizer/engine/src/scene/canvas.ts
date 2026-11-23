import { CircleGeometry, OrthographicCamera, Scene } from "three";
import type { Rendering } from "@/animation";
import { type Bounds, type CameraBox, cameraBox } from "@/view";
import { DotsLayer } from "@/scene/dots";
import type { Layer, Viewport } from "@/scene/layer";
import { LinesLayer } from "@/scene/lines";
import { type SceneRenderer, webGLRendererOn } from "@/scene/renderer";

const CIRCLE_SEGMENTS = 24;

/**
 * Draws renderings on a canvas through three.js. The canvas keeps its size on screen, and each
 * `draw` replaces what the previous one drew.
 */
export class SceneCanvas {
    readonly #scene = new Scene();
    readonly #camera = new OrthographicCamera();
    readonly #circle = new CircleGeometry(1, CIRCLE_SEGMENTS);
    readonly #layers: Layer[] = [];

    constructor(private readonly renderer: SceneRenderer) {}

    /**
     * Creates a scene canvas that draws with WebGL on the canvas.
     */
    static on(canvas: HTMLCanvasElement): SceneCanvas {
        return new SceneCanvas(webGLRendererOn(canvas));
    }

    /**
     * Draws the renderings in order, each later one on top, with all of `bounds` in view and
     * `padding` CSS pixels left free around it.
     */
    draw({ renderings, bounds, padding }: { renderings: readonly Rendering[]; bounds: Bounds; padding: number }): void {
        const viewport = this.#fitView(bounds, padding);
        this.#removeLayersFrom(renderings.length);
        renderings.forEach((rendering, order) => {
            const shownByCurrentLayer = this.#layers[order]?.show(rendering, viewport) === true;
            if (!shownByCurrentLayer) this.#replaceLayer(order, rendering).show(rendering, viewport);
        });
        this.renderer.render(this.#scene, this.#camera);
    }

    /**
     * Releases the GPU resources of the canvas.
     */
    dispose(): void {
        this.#removeLayersFrom(0);
        this.#circle.dispose();
        this.renderer.dispose();
    }

    #fitView(bounds: Bounds, padding: number): Viewport {
        const { clientWidth, clientHeight } = this.renderer.canvas;
        const width = Math.max(1, clientWidth);
        const height = Math.max(1, clientHeight);
        this.renderer.fitDrawingTo({ width, height });
        const box = cameraBox({ bounds, width, height, padding });
        this.#pointCameraAt(box);
        return { box, width, height };
    }

    #pointCameraAt({ left, right, top, bottom }: CameraBox): void {
        Object.assign(this.#camera, { left, right, top, bottom, near: -1, far: 1 });
        this.#camera.updateProjectionMatrix();
    }

    #replaceLayer(order: number, rendering: Rendering): Layer {
        const replaced = this.#layers[order];
        if (replaced !== undefined) this.#removeLayer(replaced);
        const layer = this.#createLayerFor(rendering);
        layer.object.renderOrder = order;
        this.#layers[order] = layer;
        this.#scene.add(layer.object);
        return layer;
    }

    #createLayerFor(rendering: Rendering): Layer {
        return rendering.kind === "lines" ? new LinesLayer() : new DotsLayer(this.#circle);
    }

    #removeLayersFrom(start: number): void {
        for (const layer of this.#layers.splice(start)) this.#removeLayer(layer);
    }

    #removeLayer(layer: Layer): void {
        this.#scene.remove(layer.object);
        layer.dispose();
    }
}
