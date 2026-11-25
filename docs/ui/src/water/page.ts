import { prefersReducedMotion } from "svelte/motion";
import type { ViewportPoint } from "@/water/grid";
import type { WaterPage } from "@/water/surface";

const LIGHT: readonly [number, number, number] = [0.84, 0.85, 1];
const DEFAULT_STRENGTH = 0.3;

/**
 * Starts the water surface on `canvas`, unless the reader prefers reduced motion or the browser
 * lacks WebGL2. Loads the surface on first use. Returns a function that stops it.
 */
export function startWaterOn(canvas: HTMLCanvasElement): () => void {
    const canRipple = !prefersReducedMotion.current && "WebGL2RenderingContext" in window;
    if (!canRipple) return () => {};
    const started = import("@/water/surface").then(({ WaterSurface }) => new WaterSurface(canvas, { tint: LIGHT, page: markedPage }).start());
    return () => void started.then((stop) => stop());
}

const markedPage: WaterPage = {
    strengthAt(point) {
        const area = closestAt<HTMLElement>(point, "[data-water-strength]");
        return area === undefined ? DEFAULT_STRENGTH : Number(area.dataset.waterStrength);
    },
    pressDropsAt(point) {
        return closestAt(point, "[data-water-ignores-presses]") === undefined;
    },
};

function closestAt<Found extends Element = Element>({ x, y }: ViewportPoint, selector: string): Found | undefined {
    return document.elementFromPoint(x, y)?.closest<Found>(selector) ?? undefined;
}
