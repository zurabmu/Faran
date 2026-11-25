import type { Color, LinePattern } from "@/animation";

/**
 * The dash and gap lengths of a line, in screen points. A solid line has none.
 */
export type Dashes = [] | [dash: number, gap: number];

/**
 * Returns the CSS color for an RGBA color with channels from 0 to 255.
 */
export function cssColor([red, green, blue, alpha]: Color): string {
    return `rgba(${red}, ${green}, ${blue}, ${Math.round((alpha / 255) * 1000) / 1000})`;
}

/**
 * Returns the values of the CSS custom properties on `element`, under the keys of `properties`.
 * Throws when a property has no value.
 */
export function customPropertiesOf<Key extends string>(element: Element, properties: Record<Key, `--${string}`>): Record<Key, string> {
    const style = getComputedStyle(element);
    const entries = Object.entries<string>(properties).map(([key, property]) => [key, valueOf(style, property)]);
    return Object.fromEntries(entries) as Record<Key, string>;
}

function valueOf(style: CSSStyleDeclaration, property: string): string {
    const value = style.getPropertyValue(property).trim();
    if (value === "") throw new Error(`Expected the CSS custom property ${property} to have a value, but it has none.`);
    return value;
}

/**
 * Returns the dashes of a line of the given width.
 */
export function dashesFor(pattern: LinePattern, width: number): Dashes {
    if (pattern === "dashed") return [width * 3.5, width * 2.5];
    if (pattern === "dotted") return [width, width * 2.5];
    return [];
}
