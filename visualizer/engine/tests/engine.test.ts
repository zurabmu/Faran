import { describe, expect, it } from "vitest";
import { boundsOf, cssColor, Playback } from "@faran/engine";
import { dots, lines, square } from "@test/dsl/renderings";
import { StubFrames } from "@test/stubs/frames";

describe("view", () => {
    it("bounds cover lines and dots alike", () => {
        expect(boundsOf([lines([square({ side: 10 })]), dots([[-5, 20]])])).toEqual({ left: -5, right: 10, bottom: 0, top: 20 });
    });
});

describe("style", () => {
    it("colors keep their alpha", () => {
        expect(cssColor([255, 128, 0, 51])).toBe("rgba(255, 128, 0, 0.2)");
    });
});

describe("playback", () => {
    it("seeking stays within the steps of the animation", () => {
        const playback = new Playback({ stepCount: 10, timeStep: 0.1 });

        playback.seek(42);

        expect(playback.step).toBe(9);
    });

    it("an animation needs at least one step", () => {
        expect(() => new Playback({ stepCount: 0, timeStep: 0.1 })).toThrow("at least one step");
    });

    it("playback at twice the speed covers twice as many steps in the same time", () => {
        expect(stepsPlayedInOneSecond({ speed: 2 })).toBe(2 * stepsPlayedInOneSecond({ speed: 1 }));
    });

    it("playback stops calling a listener once it is removed", () => {
        const playback = new Playback({ stepCount: 10, timeStep: 0.1 });
        let called = false;
        const remove = playback.onChange(() => {
            called = true;
        });

        remove();
        playback.seek(3);

        expect(called).toBe(false);
    });
});

function stepsPlayedInOneSecond({ speed }: { speed: number }): number {
    const frames = new StubFrames();
    const playback = new Playback({ stepCount: 100, timeStep: 0.1, clock: frames });
    playback.speed = speed;

    playback.play();
    frames.showFrameAt(1000);

    return playback.step;
}
