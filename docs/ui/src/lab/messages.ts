import type { Frame } from "@engine";

/**
 * One planner step of a demo. `frame` holds the parts that move, in meters, and `progress` is
 * the share of the goal reached, from 0 to 1.
 */
export interface LabStep {
    readonly frame: Frame;
    readonly step: number;
    readonly speed: number;
    readonly progress: number;
    readonly planningMilliseconds: number;
    readonly finished: boolean;
    readonly reachedGoal: boolean;
}

/**
 * Receives what the lab worker reports while it loads and runs a demo.
 */
export interface LabReceiver {
    onStatus(text: string): void;
    /**
     * Receives the parts of a demo that do not move, in meters.
     */
    onBackground(background: Frame): void;
    onStep(step: LabStep): void;
}
