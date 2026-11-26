/**
 * Eases `x` from 0 to 1 with zero slope at both ends. Values outside [0, 1] are clamped.
 */
export function smoothstep(x: number): number {
    const clamped = Math.min(1, Math.max(0, x));
    return clamped * clamped * (3 - 2 * clamped);
}
