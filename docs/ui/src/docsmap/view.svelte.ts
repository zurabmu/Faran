import type { Bounds, Rendering } from "@engine";
import { whenVisible } from "@/shared/dom/visibility";
import { dropOnWater } from "@/water";
import { type Destination, type MapLayout, mapLayout } from "@/docsmap/layout";
import { type Marker, markersOf, type Position, startPosition } from "@/docsmap/markers";
import { PressAnimation } from "@/docsmap/press.svelte";
import { MapSession } from "@/docsmap/session.svelte";

const HOME_DROP_STRENGTH = 0.8;
const START_MARGIN = "200px";

/**
 * The state of a docs map.
 */
export class MapView {
    readonly layout: MapLayout;
    readonly markers: readonly Marker[];
    readonly home: number;
    readonly homePosition: Position;
    readonly session: MapSession;
    readonly homePress = new PressAnimation();

    constructor(destinations: readonly Destination[]) {
        this.layout = mapLayout(destinations.length);
        this.markers = markersOf(destinations, this.layout);
        this.home = destinations.length;
        this.homePosition = startPosition(this.layout);
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
