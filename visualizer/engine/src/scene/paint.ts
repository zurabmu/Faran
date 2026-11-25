import { SRGBColorSpace } from "three";
import type { LineMaterial } from "three/addons/lines/LineMaterial.js";
import type { MeshBasicMaterial } from "three";
import type { Color } from "@engine/animation";

/**
 * Sets the color and opacity of a material to an RGBA color with channels from 0 to 255.
 */
export function paint(material: LineMaterial | MeshBasicMaterial, [red, green, blue, alpha]: Color): void {
    material.color.setRGB(red / 255, green / 255, blue / 255, SRGBColorSpace);
    material.opacity = alpha / 255;
}
