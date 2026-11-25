import { markDrawing } from "@/mark/drawing";

/**
 * Writes the Faran mark as a standalone SVG document, without animation, for use outside the
 * documentation pages.
 */
export function markSvg(): string {
    const drawing = markDrawing();
    const bodies = drawing.bodies.map((body) => `<path d="${body.outline}" fill="${body.color}"/>`).join("");
    return [
        `<svg xmlns="http://www.w3.org/2000/svg" viewBox="${drawing.viewBox}" role="img" aria-label="Faran logo"><title>Faran</title>`,
        bodies,
        "</svg>\n",
    ].join("");
}
