import { listen, stopAll } from "@/shared/dom/events";
import { type Drop, listenForDrops } from "@/water/drops";
import { ViewportGrid, type ViewportPoint } from "@/water/grid";
import { SurfaceShading } from "@/water/shading";
import { PointerTrail } from "@/water/trail";

const STEPS_PER_FRAME = 2;
const REST_PEAK = 0.006;
const DROP_RADIUS = 1.8;
const DROP_AMOUNT = 0.9;
const PRESS_STRENGTH = 1;
const LARGEST_PIXEL_RATIO = 1.5;

/**
 * How the page shapes the water: the strength of disturbances at a point of the viewport, from 0
 * to 1, and whether a press at a point lets a drop fall.
 */
export interface WaterPage {
    strengthAt(point: ViewportPoint): number;
    pressDropsAt(point: ViewportPoint): boolean;
}

/**
 * Runs the water surface behind the page.
 */
export class WaterSurface {
    readonly #grid = new ViewportGrid();
    readonly #trail = new PointerTrail(this.#grid);
    readonly #shading: SurfaceShading;
    #frame = 0;
    #running = false;

    readonly #page: WaterPage;

    constructor(
        private readonly canvas: HTMLCanvasElement,
        { tint, page }: { tint: readonly [number, number, number]; page: WaterPage },
    ) {
        this.#shading = new SurfaceShading(canvas, { tint });
        this.#page = page;
    }

    /**
     * Starts listening for input. Returns a function that stops listening and drawing.
     */
    start(): () => void {
        this.#resize();
        return stopAll([
            listen(window, "resize", () => this.#resize(), {}),
            listen(window, "scroll", () => this.#followScroll(), { passive: true }),
            listen(window, "pointermove", (event) => this.#followPointer(event), { passive: true }),
            listen(window, "pointerdown", (event) => this.#dropOnPress(event), { passive: true }),
            listen(document, "pointerleave", () => this.#trail.lift(), {}),
            listenForDrops((drop) => this.#drop(drop)),
            () => this.#sleep(),
        ]);
    }

    #resize(): void {
        this.#grid.resize();
        this.#shading.resize(Math.min(window.devicePixelRatio || 1, LARGEST_PIXEL_RATIO));
        this.#shading.clear();
        this.#followScroll();
    }

    #followScroll(): void {
        this.#grid.followScroll();
        this.canvas.style.transform = `translateY(${this.#grid.canvasOffset}px)`;
    }

    #followPointer(event: PointerEvent): void {
        const isTouch = event.pointerType === "touch";
        if (isTouch) return;
        const point = pointOf(event);
        if (this.#trail.moveTo(point, this.#page.strengthAt(point))) this.#wake();
    }

    #dropOnPress(event: PointerEvent): void {
        const point = pointOf(event);
        if (this.#page.pressDropsAt(point)) this.#drop({ ...point, strength: PRESS_STRENGTH });
    }

    #drop({ x, y, strength }: Drop): void {
        const point = { x, y };
        this.#grid.disturbAt(point, { radius: DROP_RADIUS, amount: DROP_AMOUNT * strength * this.#page.strengthAt(point) });
        this.#wake();
    }

    #wake(): void {
        if (this.#running) return;
        this.#running = true;
        this.#frame = requestAnimationFrame(() => this.#advance());
    }

    #advance(): void {
        const { field } = this.#grid;
        for (let step = 0; step < STEPS_PER_FRAME; step += 1) field.step();
        this.#shading.draw(field);
        const isAtRest = field.peak() < REST_PEAK;
        if (isAtRest) this.#rest();
        else this.#frame = requestAnimationFrame(() => this.#advance());
    }

    #rest(): void {
        this.#running = false;
        this.#shading.clear();
    }

    #sleep(): void {
        cancelAnimationFrame(this.#frame);
        this.#running = false;
    }
}

function pointOf(event: PointerEvent): ViewportPoint {
    return { x: event.clientX, y: event.clientY };
}
