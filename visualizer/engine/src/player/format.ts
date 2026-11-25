const SIGNIFICANT_DIGITS = 3;

/**
 * Returns a value as the player shows it, rounded to three significant digits.
 */
export function formatValue(value: number): string {
    return Number(value.toPrecision(SIGNIFICANT_DIGITS)).toString();
}
