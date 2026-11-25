import uPlot from "uplot";
import type { Chart, ChartLine } from "@/animation";
import type { SizeWatcher } from "@/size";
import { cssColor, customPropertiesOf, dashesFor } from "@/style";

const LINEAR_DISTRIBUTION = 1;
const LOG_DISTRIBUTION = 3;
const LABEL_FONT_SIZE = "10px";
const AXIS_SIZE = 34;

/**
 * The colors a chart draws its axes, grid and step cursor with, and the font of its labels.
 */
export interface ChartTheme {
    readonly axis: string;
    readonly grid: string;
    readonly label: string;
    readonly cursor: string;
    readonly font: string;
}

/**
 * What the pointer does on a chart, by step.
 */
export interface ChartPointer {
    hover(step: number): void;
    leave(): void;
    seek(step: number): void;
}

/**
 * A chart of every line over all steps, with a cursor at the shown step. It fills its container,
 * reports the step under the pointer to `pointer`, and seeks to the step that a press or a drag
 * is at.
 */
export class ChartPlot {
    readonly #container: HTMLElement;
    readonly #plot: uPlot;
    readonly #stopWatchingSize: () => void;
    #step = 0;

    constructor({ container, chart, theme, watchSize, pointer }: { container: HTMLElement; chart: Chart; theme: ChartTheme; watchSize: SizeWatcher; pointer: ChartPointer }) {
        this.#container = container;
        const axis = axisStyle(theme);
        this.#plot = new uPlot(
            {
                ...this.#containerSize(),
                legend: { show: false },
                cursor: { y: false, drag: { x: false, y: false, setScale: false } },
                scales: { x: { time: false }, y: { distr: chart.scale === "log" ? LOG_DISTRIBUTION : LINEAR_DISTRIBUTION } },
                axes: [{ ...axis, show: false }, axis],
                series: [{}, ...chart.lines.map(lineSeries)],
                plugins: [{ hooks: { draw: (plot: uPlot) => drawCursor(plot, this.#step, theme.cursor), setCursor: (plot: uPlot) => reportHover(plot, pointer) } }],
            },
            [stepsOf(chart), ...chart.lines.map((line) => [...line.values])],
            container,
        );
        this.#stopWatchingSize = watchSize(() => this.#fitContainer());
        seekOnPress(this.#plot, pointer);
    }

    /**
     * Moves the cursor to `step`.
     */
    show(step: number): void {
        this.#step = step;
        this.#plot.redraw(false, false);
    }

    destroy(): void {
        this.#stopWatchingSize();
        this.#plot.destroy();
    }

    #fitContainer(): void {
        this.#plot.setSize(this.#containerSize());
    }

    #containerSize(): { width: number; height: number } {
        return { width: Math.max(1, this.#container.clientWidth), height: Math.max(1, this.#container.clientHeight) };
    }
}

/**
 * Returns the chart theme from the custom properties that the player defines for `element`, and
 * from the font family of `element`.
 */
export function chartThemeOf(element: HTMLElement): ChartTheme {
    const colors = customPropertiesOf(element, { axis: "--rule-strong", grid: "--rule", label: "--faint", cursor: "--accent" });
    return { ...colors, font: `${LABEL_FONT_SIZE} ${getComputedStyle(element).fontFamily}` };
}

function stepsOf(chart: Chart): number[] {
    const stepCount = chart.lines.reduce((longest, line) => Math.max(longest, line.values.length), 1);
    return Array.from({ length: stepCount }, (_, index) => index);
}

function axisStyle(theme: ChartTheme): uPlot.Axis {
    return {
        stroke: theme.label,
        grid: { stroke: theme.grid, width: 1 },
        ticks: { stroke: theme.axis, width: 1 },
        font: theme.font,
        size: AXIS_SIZE,
    };
}

function lineSeries(line: ChartLine): uPlot.Series {
    return {
        label: line.name,
        stroke: cssColor(line.style.color),
        width: line.style.width,
        dash: dashesFor(line.style.pattern, line.style.width),
        points: { show: false },
    };
}

function reportHover(plot: uPlot, pointer: ChartPointer): void {
    const step = plot.cursor.idx;
    const isOverChart = step !== null && step !== undefined;
    if (isOverChart) pointer.hover(step);
    else pointer.leave();
}

function seekOnPress(plot: uPlot, pointer: ChartPointer): void {
    const seekAt = (event: PointerEvent) => pointer.seek(plot.posToVal(event.offsetX, "x"));
    plot.over.addEventListener("pointerdown", (event) => {
        plot.over.setPointerCapture(event.pointerId);
        seekAt(event);
    });
    plot.over.addEventListener("pointermove", (event) => {
        const isDragging = plot.over.hasPointerCapture(event.pointerId);
        if (isDragging) seekAt(event);
    });
}

function drawCursor(plot: uPlot, step: number, color: string): void {
    const x = plot.valToPos(step, "x", true);
    const { top, height } = plot.bbox;
    strokeLine(plot.ctx, { from: [x, top], to: [x, top + height], color, width: uPlot.pxRatio });
}

function strokeLine(
    context: CanvasRenderingContext2D,
    { from, to, color, width }: { from: [number, number]; to: [number, number]; color: string; width: number },
): void {
    context.save();
    context.strokeStyle = color;
    context.lineWidth = width;
    context.beginPath();
    context.moveTo(...from);
    context.lineTo(...to);
    context.stroke();
    context.restore();
}
