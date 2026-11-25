import { CircleGeometry, OrthographicCamera, Scene } from "three";
import type { Rendering } from "@engine/animation";
import { type Bounds, type CameraBox, cameraBox } from "@engine/view";
import { DotsLayer } from "@engine/scene/dots";
import type { Layer, Viewport } from "@engine/scene/layer";
import { LinesLayer } from "@engine/scene/lines";
import { type SceneRenderer, webGLRendererOn } from "@engine/scene/renderer";
import { type SizeWatcher, sizeWatcherOf } from "@engine/size";

const CIRCLE_SEGMENTS = 24;

/**
 * Renderings in drawing order, the `bounds` to keep in view, and `padding` in CSS pixels to
 * leave free around them.
 */
export interface Drawing {
    readonly renderings: readonly Rendering[];
    readonly bounds: Bounds;
    readonly padding: number;
}

/**
 * Draws renderings on a canvas with three.js. Each `draw` replaces the previous drawing, which
 * is drawn again whenever the canvas changes size.
 */
export class SceneCanvas {
    readonly #scene = new Scene();
    readonly #camera = new OrthographicCamera();
    readonly #circle = new CircleGeometry(1, CIRCLE_SEGMENTS);
    readonly #layers: Layer[] = [];
    readonly #stopWatchingSize: () => void;
    #redraw: () => void = () => {};

    constructor(
        private readonly renderer: SceneRenderer,
        watchSize: SizeWatcher,
    ) {
        this.#stopWatchingSize = watchSize(() => this.#redraw());
    }

    /**
     * Creates a scene canvas that draws with WebGL on the canvas.
     */
    static on(canvas: HTMLCanvasElement): SceneCanvas {
        return new SceneCanvas(webGLRendererOn(canvas), sizeWatcherOf(canvas));
    }

    draw(drawing: Drawing): void {
        this.#redraw = () => this.#render(drawing);
        this.#render(drawing);
    }

    /**
     * Releases the GPU resources of the canvas and stops watching its size.
     */
    dispose(): void {
        this.#stopWatchingSize();
        this.#removeLayersFrom(0);
        this.#circle.dispose();
        this.renderer.dispose();
    }

    #render({ renderings, bounds, padding }: Drawing): void {
        const viewport = this.#fitView(bounds, padding);
        this.#removeLayersFrom(renderings.length);
        renderings.forEach((rendering, order) => {
            const shownByCurrentLayer = this.#layers[order]?.show(rendering, viewport) === true;
            if (!shownByCurrentLayer) this.#replaceLayer(order, rendering).show(rendering, viewport);
        });
        this.renderer.render(this.#scene, this.#camera);
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
