import type { Frame } from "@engine";

/**
 * The smallest time between two planner steps, in milliseconds.
 */
export const STEP_MILLISECONDS = 45;

/**
 * The frames of the moving parts at the start and the end of a planner step. Both have the same
 * renderings with the same number of points.
 */
export interface Motion {
    readonly start: Frame;
    readonly end: Frame;
}

/**
 * The parts of the docs map that the planner needs, in field units with y pointing up.
 */
export interface NavigationLayout {
    readonly places: readonly (readonly [number, number])[];
    readonly obstacles: readonly { readonly center: readonly [number, number]; readonly radius: number }[];
    readonly start: { readonly x: number; readonly y: number; readonly heading: number };
}

/**
 * One planner step of the docs map. `milliseconds` is how long the planner took.
 */
export interface NavigationStep {
    readonly frame: Frame;
    readonly motion: Motion;
    readonly milliseconds: number;
}
