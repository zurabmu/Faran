import type { Frame } from "@engine";
import { expose } from "comlink";
import { labExport } from "@/shared/python";
import { wait } from "@/shared/wait";
import { type Motion, type NavigationLayout, type NavigationStep, STEP_MILLISECONDS } from "@/docsmap/messages";

interface Navigation {
    background(): string;
    aim(place: number): void;
    advance(): string;
}

interface NavigationFactory {
    from_layout(layout: string): Navigation;
}

interface Advanced {
    readonly frame: Frame;
    readonly motion: Motion;
    readonly moving: boolean;
    readonly fading: boolean;
}

const loadNavigationFactory = labExport<NavigationFactory>("Navigation");
let navigation: Promise<Navigation> | undefined;
let running = false;

const navigationWorker = {
    /**
     * Loads the planner for `layout` on the first call and returns the frame of the obstacles.
     * `report` receives status texts.
     */
    async start(options: { assetsUrl: string; layout: NavigationLayout }, report: (text: string) => void): Promise<Frame> {
        navigation ??= createNavigation(options, report);
        return JSON.parse((await navigation).background()) as Frame;
    },

    /**
     * Calls `show` with every planner step towards the place until the robot has arrived and its
     * trail has faded, or only with the last step when `instantly` is set.
     */
    async aim({ place, instantly }: { place: number; instantly: boolean }, show: (step: NavigationStep) => void): Promise<void> {
        if (navigation === undefined) throw new Error("The docs map worker got a place to aim at before it was started.");
        const planner = await navigation;
        planner.aim(place);
        if (instantly) return showLastStep(planner, show);
        if (running) return;
        running = true;
        await showEveryStep(planner, show);
        running = false;
    },
};

/**
 * The docs map planner that `docsmap/worker.ts` exposes with Comlink.
 */
export type NavigationWorker = typeof navigationWorker;

expose(navigationWorker);

async function createNavigation({ assetsUrl, layout }: { assetsUrl: string; layout: NavigationLayout }, report: (text: string) => void): Promise<Navigation> {
    const factory = await loadNavigationFactory({ assetsUrl, report });
    return factory.from_layout(JSON.stringify(layout));
}

function showLastStep(planner: Navigation, show: (step: NavigationStep) => void): void {
    let advanced = advance(planner);
    while (advanced.moving) advanced = advance(planner);
    show({ frame: advanced.frame, motion: advanced.motion, milliseconds: 0 });
}

async function showEveryStep(planner: Navigation, show: (step: NavigationStep) => void): Promise<void> {
    for (;;) {
        const started = performance.now();
        const advanced = advance(planner);
        show({ frame: advanced.frame, motion: advanced.motion, milliseconds: performance.now() - started });
        const isSettled = !advanced.moving && !advanced.fading;
        if (isSettled) return;
        await wait(Math.max(0, STEP_MILLISECONDS - (performance.now() - started)));
    }
}

function advance(planner: Navigation): Advanced {
    return JSON.parse(planner.advance()) as Advanced;
}
