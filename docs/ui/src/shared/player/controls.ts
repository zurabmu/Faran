/**
 * A player that the player controls show and drive. `seconds` and `endSeconds` are simulation
 * time, and `speed` is a multiple of real time.
 */
export interface PlayerControls {
    readonly ready: boolean;
    readonly playing: boolean;
    readonly step: number;
    readonly first: number;
    readonly last: number;
    readonly seconds: number;
    readonly endSeconds: number;
    readonly speed: number;
    toggle(): void;

    /**
     * Pauses at `step`, clamped to the recorded steps.
     */
    seek(step: number): void;

    /**
     * Pauses `count` steps from the current one, backwards for a negative count.
     */
    stepBy(count: number): void;
    changeSpeed(speed: number): void;
}

/**
 * Whether `player` has more than one step to move between. A player that is not ready yet may
 * still get them.
 */
export function hasSteps(player: PlayerControls): boolean {
    return !player.ready || player.last > player.first;
}

/**
 * How far `player` is from its first step to its last, in percent.
 */
export function progressOf(player: PlayerControls): number {
    const span = player.last - player.first;
    return span > 0 ? ((player.step - player.first) / span) * 100 : 0;
}
