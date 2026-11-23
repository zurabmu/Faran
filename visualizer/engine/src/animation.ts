/**
 * A point in the x-y plane, in the units of the scene.
 */
export type Point = readonly [number, number];

/**
 * A color as red, green, blue and alpha, each from 0 to 255.
 */
export type Color = readonly [number, number, number, number];

export type LinePattern = "solid" | "dashed" | "dotted";

/**
 * How lines are drawn. `width` is in screen points.
 */
export interface LineStyle {
    readonly color: Color;
    readonly width: number;
    readonly pattern: LinePattern;
}

/**
 * Polylines through the points of each strip.
 */
export interface Lines {
    readonly kind: "lines";
    readonly name: string;
    readonly strips: readonly (readonly Point[])[];
    readonly style: LineStyle;
}

/**
 * A dot at each position. `size` is the dot diameter in screen points.
 */
export interface Dots {
    readonly kind: "dots";
    readonly name: string;
    readonly positions: readonly Point[];
    readonly style: { readonly color: Color; readonly size: number };
}

export type Rendering = Lines | Dots;

/**
 * A line sample in a legend entry. `width` is in screen points.
 */
export interface LineMark {
    readonly kind: "line";
    readonly color: Color;
    readonly width: number;
    readonly pattern: LinePattern;
}

/**
 * A dot in a legend entry. `size` is the dot diameter in screen points.
 */
export interface DotMark {
    readonly kind: "dot";
    readonly color: Color;
    readonly size: number;
}

export type Mark = LineMark | DotMark;

/**
 * A legend entry: a label, and the marks that draw its sample, lines below dots.
 */
export interface LegendEntry {
    readonly label: string;
    readonly marks: readonly Mark[];
}

/**
 * A row of the info table at one step. `unit` is empty when the value has none.
 */
export interface Row {
    readonly label: string;
    readonly value: number;
    readonly unit: string;
}

/**
 * What is shown at one step. Later renderings are drawn on top.
 */
export interface Frame {
    readonly renderings: readonly Rendering[];
    readonly info: readonly Row[];
}

/**
 * One line of a chart, with one value per step.
 */
export interface ChartLine {
    readonly name: string;
    readonly values: readonly number[];
    readonly style: LineStyle;
}

export interface Chart {
    readonly id: string;
    readonly title: string;
    readonly yLabel: string;
    readonly scale: "linear" | "log";
    readonly lines: readonly ChartLine[];
}

/**
 * An animation as the canvas renderer of `faran_visualizer` saves it. Background renderings
 * are drawn below the renderings of every frame, on the background color. The legend has one
 * entry per label.
 */
export interface Animation {
    readonly timeStep: number;
    readonly backgroundColor: Color;
    readonly background: readonly Rendering[];
    readonly frames: readonly Frame[];
    readonly charts: readonly Chart[];
    readonly legend: readonly LegendEntry[];
}
