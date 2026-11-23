import { type Camera, type Object3D, Vector2, WebGLRenderer } from "three";

/**
 * Draws a three.js scene onto a canvas.
 */
export interface SceneRenderer {
    /**
     * The canvas, whose size on screen in CSS pixels the page layout decides.
     */
    readonly canvas: { readonly clientWidth: number; readonly clientHeight: number };

    /**
     * Makes the drawing as sharp as the screen allows on a canvas of this size on screen, in CSS
     * pixels.
     */
    fitDrawingTo(size: { width: number; height: number }): void;
    render(scene: Object3D, camera: Camera): void;
    dispose(): void;
}

/**
 * Creates a renderer that draws with WebGL on the canvas, with a transparent background, at the
 * pixel ratio of the screen the page is on.
 */
export function webGLRendererOn(canvas: HTMLCanvasElement): SceneRenderer {
    return new WebGLSceneRenderer(canvas);
}

class WebGLSceneRenderer implements SceneRenderer {
    readonly #renderer: WebGLRenderer;
    readonly #size = new Vector2();

    constructor(readonly canvas: HTMLCanvasElement) {
        this.#renderer = new WebGLRenderer({ canvas, antialias: true, alpha: true });
        this.#renderer.setClearColor(0x000000, 0);
    }

    fitDrawingTo({ width, height }: { width: number; height: number }): void {
        this.#matchScreenPixelRatio();
        this.#matchDrawingBufferSize(width, height);
    }

    render(scene: Object3D, camera: Camera): void {
        this.#renderer.render(scene, camera);
    }

    dispose(): void {
        this.#renderer.dispose();
    }

    #matchScreenPixelRatio(): void {
        const pixelRatio = window.devicePixelRatio || 1;
        const pixelRatioChanged = pixelRatio !== this.#renderer.getPixelRatio();
        if (pixelRatioChanged) this.#renderer.setPixelRatio(pixelRatio);
    }

    #matchDrawingBufferSize(width: number, height: number): void {
        const size = this.#renderer.getSize(this.#size);
        const sizeChanged = size.x !== width || size.y !== height;
        if (sizeChanged) this.#renderer.setSize(width, height, false);
    }
}
