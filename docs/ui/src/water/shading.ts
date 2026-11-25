import {
    DataTexture,
    FloatType,
    GLSL3,
    LinearFilter,
    Mesh,
    NoBlending,
    OrthographicCamera,
    PlaneGeometry,
    RawShaderMaterial,
    RedFormat,
    Vector2,
    Vector3,
    WebGLRenderer,
} from "three";
import fragmentShader from "@/water/shaders/surface.frag?raw";
import vertexShader from "@/water/shaders/surface.vert?raw";

/**
 * A grid of heights in row-major order, top row first.
 */
export interface HeightGrid {
    readonly heights: Float32Array;
    readonly columns: number;
    readonly rows: number;
}

/**
 * Draws a height field as light on a water surface. A flat surface draws nothing.
 */
export class SurfaceShading {
    readonly #renderer: WebGLRenderer;
    readonly #camera = new OrthographicCamera();
    readonly #surface: Mesh;
    readonly #uniforms: { heights: { value: DataTexture }; texel: { value: Vector2 }; tint: { value: Vector3 } };

    constructor(
        private readonly canvas: HTMLCanvasElement,
        { tint }: { tint: readonly [number, number, number] },
    ) {
        this.#renderer = new WebGLRenderer({ canvas, alpha: true, premultipliedAlpha: true, antialias: false });
        this.#renderer.setClearColor(0x000000, 0);
        this.#uniforms = { heights: { value: heightTexture(1, 1) }, texel: { value: new Vector2(1, 1) }, tint: { value: new Vector3(...tint) } };
        this.#surface = fullScreenQuad(
            // The shader writes premultiplied colors, which the canvas shows as they are.
            new RawShaderMaterial({ glslVersion: GLSL3, vertexShader, fragmentShader, uniforms: this.#uniforms, blending: NoBlending, depthTest: false }),
        );
    }

    /**
     * Matches the drawing buffer to the canvas size on screen, at the given pixels per CSS pixel.
     */
    resize(scale: number): void {
        this.#renderer.setPixelRatio(scale);
        this.#renderer.setSize(this.canvas.clientWidth, this.canvas.clientHeight, false);
    }

    draw(grid: HeightGrid): void {
        this.#upload(grid);
        this.#renderer.render(this.#surface, this.#camera);
    }

    clear(): void {
        this.#renderer.clear();
    }

    #upload({ heights, columns, rows }: HeightGrid): void {
        const texture = this.#uniforms.heights.value;
        const sizeChanged = texture.image.width !== columns || texture.image.height !== rows;
        if (sizeChanged) this.#replaceTexture(columns, rows);
        this.#uniforms.heights.value.image.data = heights;
        this.#uniforms.heights.value.needsUpdate = true;
    }

    #replaceTexture(columns: number, rows: number): void {
        this.#uniforms.heights.value.dispose();
        this.#uniforms.heights.value = heightTexture(columns, rows);
        this.#uniforms.texel.value.set(1 / columns, 1 / rows);
    }
}

function fullScreenQuad(material: RawShaderMaterial): Mesh {
    const quad = new Mesh(new PlaneGeometry(2, 2), material);
    // The vertex shader places the quad on the whole canvas, whatever the camera sees.
    quad.frustumCulled = false;
    return quad;
}

function heightTexture(columns: number, rows: number): DataTexture {
    const texture = new DataTexture(new Float32Array(columns * rows), columns, rows, RedFormat, FloatType);
    // A half float texture filters linearly in every WebGL2 browser, which a full float one does not.
    texture.internalFormat = "R16F";
    texture.minFilter = LinearFilter;
    texture.magFilter = LinearFilter;
    texture.unpackAlignment = 1;
    return texture;
}
