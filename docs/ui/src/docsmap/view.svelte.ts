import type { Bounds, Rendering } from "@engine";
import { whenVisible } from "@/shared/dom/visibility";
import { dropOnWater } from "@/water";
import { type Destination, type MapLayout, tallMapLayout, wideMapLayout } from "@/docsmap/layout";
import { type Labeling, labelsAround, labelsBeside, type Marker, markersOf, type Placement } from "@/docsmap/markers";
import { PressAnimation } from "@/docsmap/press.svelte";
import { MapSession } from "@/docsmap/session.svelte";

interface MapShape {
    readonly tall: boolean;
    readonly layout: (count: number) => MapLayout;
    readonly labeling: Labeling;
}

const WIDE: MapShape = { tall: false, layout: wideMapLayout, labeling: labelsAround };
const TALL: MapShape = { tall: true, layout: tallMapLayout, labeling: labelsBeside };
const NARROW_SCREEN = "screen and (max-width: 44.984375em)";
const HOME_DROP_STRENGTH = 0.8;
const START_MARGIN = "200px";

/**
 * The state of a docs map.
 */
export class MapView {
    readonly tall: boolean;
    readonly layout: MapLayout;
    readonly markers: readonly Marker[];
    readonly home: number;
    readonly homePlacement: Placement;
    readonly session: MapSession;
    readonly homePress = new PressAnimation();

    constructor(destinations: readonly Destination[]) {
        const shape = matchMedia(NARROW_SCREEN).matches ? TALL : WIDE;
        this.tall = shape.tall;
        this.layout = shape.layout(destinations.length);
        this.markers = markersOf({ destinations, layout: this.layout, labeling: shape.labeling });
        this.home = destinations.length;
        this.homePlacement = shape.labeling.placeHome(this.layout);
        this.session = new MapSession(this.layout);
    }

    /**
     * The renderings of the planner's latest step, over the obstacles.
     */
    get renderings(): readonly Rendering[] {
        const { background, frame, motion } = this.session;
        return [...background.renderings, ...frame.renderings, ...motion.renderings];
    }

    /**
     * The whole map, in field units.
     */
    get bounds(): Bounds {
        return { left: 0, right: this.layout.width, bottom: 0, top: this.layout.height };
    }

    /** On touch, the first tap aims and the second follows the link. */
    aimOrFollow(event: MouseEvent, index: number): void {
        const isTouch = event instanceof PointerEvent && event.pointerType === "touch";
        const isAimed = this.session.aimedAt === index;
        if (!isTouch || isAimed) return;
        event.preventDefault();
        this.session.aim(index);
    }

    aimAtPointer(event: PointerEvent, index: number): void {
        const isTouch = event.pointerType === "touch";
        if (!isTouch) this.session.aim(index);
    }

    aimAtFocus(element: HTMLElement, index: number): void {
        const isKeyboardFocus = element.matches(":focus-visible");
        if (isKeyboardFocus) this.session.aim(index);
    }

    /**
     * Aims the planner back at its start, plays the home marker's press animation and drops a
     * ripple on the page's water background where the pointer is.
     */
    pressHome(event: MouseEvent): void {
        this.session.aim(this.home);
        this.homePress.press();
        dropOnWater({ x: event.clientX, y: event.clientY, strength: HOME_DROP_STRENGTH });
    }

    /**
     * Starts the planner once `element` comes near the viewport.
     */
    startWhenVisible(element: HTMLElement): () => void {
        return whenVisible(element, { rootMargin: START_MARGIN }, () => this.session.start());
    }

    stop(): void {
        this.session.stop();
    }
}
