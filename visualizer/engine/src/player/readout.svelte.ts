import type { Chart, ChartLine } from "@/animation";
import { formatValue } from "@/player/format";
import { cssColor } from "@/style";

/**
 * The value of one chart line at a step, formatted, with the CSS color of the line.
 */
export interface LineReading {
    readonly name: string;
    readonly value: string;
    readonly color: string;
}

/**
 * The values of a chart's lines at the step under the pointer. It has no readings while the
 * pointer is off the chart.
 */
export class ChartReadout {
    step = $state(0);
    readings: readonly LineReading[] = $state([]);

    constructor(private readonly chart: () => Chart) {}

    hover(step: number): void {
        this.step = step;
        this.readings = this.chart().lines.flatMap((line) => readingsOf(line, step));
    }

    leave(): void {
        this.readings = [];
    }
}

function readingsOf(line: ChartLine, step: number): LineReading[] {
    const value = line.values[step];
    const hasValueAtStep = value !== undefined;
    return hasValueAtStep ? [{ name: line.name, value: formatValue(value), color: cssColor(line.style.color) }] : [];
}
