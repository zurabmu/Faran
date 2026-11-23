import { type Group, InstancedMesh, Matrix4, type OrthographicCamera, Vector3 } from "three";
import type { LineSegments2 } from "three/addons/lines/LineSegments2.js";
import { describe, expect, it } from "vitest";
import { type Bounds, type Point, type Rendering, SceneCanvas } from "@faran/engine";
import { dots, lines, square } from "@test/dsl/renderings";
import { StubRenderer } from "@test/stubs/renderer";

describe("lines", () => {
    it("a line connects its points in order", () => {
        const canvas = canvasOfSize();

        canvas.draw([
            lines([
                [
                    [0, 0],
                    [3, 0],
                    [3, 4],
                ],
            ]),
        ]);

        expect(canvas.picture()).toEqual([
            expect.objectContaining({
                segments: [
                    { start: [0, 0], end: [3, 0] },
                    { start: [3, 0], end: [3, 4] },
                ],
            }),
        ]);
    });

    it("a dashed line drawn after another one has the same dashes as when drawn alone", () => {
        const line: Point[] = [
            [0, 0],
            [3, 0],
            [3, 4],
        ];

        const alone = canvasThatDrew([lines([line], { pattern: "dashed" })]).dashes();
        const together = canvasThatDrew([lines([line, line], { pattern: "dashed" })]).dashes();

        expect(together).toEqual([...alone, ...alone]);
    });

    it("a line drawn after a longer one looks as it does on a fresh canvas", () => {
        const line = lines([
            [
                [5, 5],
                [6, 5],
            ],
        ]);
        const canvas = canvasOfSize();

        canvas.draw([lines([square()])]);
        canvas.draw([line]);

        expect(canvas.picture()).toEqual(canvasThatDrew([line]).picture());
    });

    it("a line drawn after a shorter one looks as it does on a fresh canvas", () => {
        const line = lines([square()]);
        const canvas = canvasOfSize();

        canvas.draw([
            lines([
                [
                    [0, 0],
                    [1, 0],
                ],
            ]),
        ]);
        canvas.draw([line]);

        expect(canvas.picture()).toEqual(canvasThatDrew([line]).picture());
    });
});

describe("dots", () => {
    it("dots sit at their positions and are as wide on screen as their size", () => {
        const canvas = canvasOfSize({ clientWidth: 100, clientHeight: 100 });

        canvas.draw([dots([[1, 2]], { size: 4 })], { bounds: squareBounds({ side: 10 }) });

        expect(canvas.picture()).toEqual([{ kind: "dots", dots: [{ center: [1, 2], widthInPixels: 4 }] }]);
    });

    it("dots keep their width on screen when the view zooms", () => {
        const canvas = canvasOfSize({ clientWidth: 100, clientHeight: 100 });
        const shown = dots([[1, 2]], { size: 4 });

        canvas.draw([shown], { bounds: squareBounds({ side: 10 }) });
        canvas.draw([shown], { bounds: squareBounds({ side: 5 }) });

        expect(canvas.picture()).toEqual([{ kind: "dots", dots: [{ center: [1, 2], widthInPixels: 4 }] }]);
    });

    it("dots drawn after fewer dots look as they do on a fresh canvas", () => {
        const shown = dots([
            [1, 0],
            [2, 0],
            [3, 0],
        ]);
        const canvas = canvasOfSize();

        canvas.draw([dots([[0, 0]])]);
        canvas.draw([shown]);

        expect(canvas.picture()).toEqual(canvasThatDrew([shown]).picture());
    });
});

describe("scene canvas", () => {
    it("the canvas draws later renderings on top", () => {
        const canvas = canvasOfSize();

        canvas.draw([lines([square()]), dots([[0, 0]]), lines([square()])]);

        expect(canvas.renderOrders()).toEqual([0, 1, 2]);
    });

    it("the canvas stops drawing renderings that a later draw leaves out", () => {
        const canvas = canvasOfSize();

        canvas.draw([lines([square()]), dots([[0, 0]]), lines([square()])]);
        canvas.draw([lines([square()])]);

        expect(canvas.picture().map(({ kind }) => kind)).toEqual(["lines"]);
    });

    it("the canvas draws dots where the previous draw had lines", () => {
        const canvas = canvasOfSize();

        canvas.draw([lines([square()])]);
        canvas.draw([dots([[0, 0]])]);

        expect(canvas.picture().map(({ kind }) => kind)).toEqual(["dots"]);
    });

    it("the canvas fits its drawing to its size on screen after the size changes", () => {
        const canvas = canvasOfSize({ clientWidth: 200, clientHeight: 100 });

        canvas.draw([lines([square()])]);
        canvas.renderer.canvas.clientWidth = 300;
        canvas.draw([lines([square()])]);

        expect(canvas.renderer.fittedSize).toEqual({ width: 300, height: 100 });
    });
});

type Drawn =
    | { kind: "lines"; segments: { start: Point; end: Point }[]; dashes: number[][] }
    | { kind: "dots"; dots: { center: Point; widthInPixels: number }[] };

function squareBounds({ side }: { side: number }): Bounds {
    return { left: 0, right: side, bottom: 0, top: side };
}

function canvasThatDrew(renderings: readonly Rendering[]) {
    const canvas = canvasOfSize();
    canvas.draw(renderings);
    return canvas;
}

/**
 * Creates a scene canvas on a canvas with the given size on screen, and reads back what its
 * renderer drew last.
 */
function canvasOfSize(size = { clientWidth: 200, clientHeight: 100 }) {
    const renderer = new StubRenderer(size);
    const scene = new SceneCanvas(renderer);
    const lastRender = () => renderer.renders.at(-1)!;
    const drawnLayers = () => lastRender().scene.children as Group[];
    const pixelsPerUnit = () => {
        const { left, right } = lastRender().camera as OrthographicCamera;
        return size.clientWidth / (right - left);
    };
    const drawnOf = (layer: Group): Drawn => {
        const content = layer.children[0]!;
        if (content instanceof InstancedMesh) return { kind: "dots", dots: dotsOf(content, pixelsPerUnit()) };
        const line = content as LineSegments2;
        return { kind: "lines", segments: segmentsOf(line), dashes: dashesOf(line) };
    };
    return {
        renderer,
        draw: (renderings: readonly Rendering[], { bounds = squareBounds({ side: 1 }) }: { bounds?: Bounds } = {}) =>
            scene.draw({ renderings, bounds, padding: 0 }),
        renderOrders: () => drawnLayers().map((layer) => layer.renderOrder),
        picture: () => drawnLayers().map(drawnOf),
        dashes: () => {
            const drawn = drawnOf(drawnLayers()[0]!);
            if (drawn.kind !== "lines") throw new Error(`Expected the first rendering drawn to be lines, but it is ${drawn.kind}.`);
            return drawn.dashes;
        },
    };
}

function segmentsOf({ geometry }: LineSegments2): { start: Point; end: Point }[] {
    const { instanceStart: start, instanceEnd: end } = geometry.attributes;
    return Array.from({ length: geometry.instanceCount }, (_, index) => ({
        start: [start!.getX(index), start!.getY(index)],
        end: [end!.getX(index), end!.getY(index)],
    }));
}

function dashesOf({ geometry }: LineSegments2): number[][] {
    const { instanceDistanceStart: start, instanceDistanceEnd: end } = geometry.attributes;
    return Array.from({ length: geometry.instanceCount }, (_, index) => [start!.getX(index), end!.getX(index)]);
}

function dotsOf(mesh: InstancedMesh, pixelsPerUnit: number): { center: Point; widthInPixels: number }[] {
    const placement = new Matrix4();
    return Array.from({ length: mesh.count }, (_, index) => {
        mesh.getMatrixAt(index, placement);
        const position = new Vector3().setFromMatrixPosition(placement);
        const radius = new Vector3().setFromMatrixScale(placement).x;
        return { center: [position.x, position.y], widthInPixels: Number((2 * radius * pixelsPerUnit).toFixed(6)) };
    });
}
