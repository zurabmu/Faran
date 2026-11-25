import { Resvg } from "@resvg/resvg-js";
import pngToIco from "png-to-ico";

/**
 * Renders an SVG document to a PNG image of the given width and height in pixels.
 */
export function renderPng(svg: string, size: number): Buffer {
    return Buffer.from(new Resvg(svg, { fitTo: { mode: "width", value: size } }).render().asPng());
}

/**
 * Packs PNG renders of an SVG document at the given sizes into one .ico file.
 */
export function icoFile(svg: string, sizes: readonly number[]): Promise<Buffer> {
    return pngToIco(sizes.map((size) => renderPng(svg, size)));
}
