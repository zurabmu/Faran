import { readFileSync } from "node:fs";
import { join } from "node:path";
import { formatPoint, type Point, smoothstep } from "@/geometry";
import { brand } from "@/shared/brand";

const STYLESHEET = join(import.meta.dirname, "spinner.css");
const END_TAPER_DEGREES = 55;
const POCKET_DEGREES = 60;
const MASK_MARGIN = 0.2;
const RING_SAMPLES = 180;
const REGION = 'maskUnits="userSpaceOnUse" x="-50" y="-50" width="100" height="100"';

interface Ring {
    readonly name: string;
    readonly radius: number;
    readonly width: number;
    readonly color: string;
    readonly clockwise: boolean;
}

const RINGS: readonly Ring[] = [
    { name: "outer", radius: 40, width: 3.6, color: brand.taken, clockwise: true },
    { name: "inner", radius: 28, width: 3, color: brand.plan, clockwise: false },
];

/**
 * Returns the loading spinner as an SVG document that animates when used as a CSS background image.
 */
export function loadingSpinnerSvg(): string {
    return [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="-50 -50 100 100">',
        `<style>${readFileSync(STYLESHEET, "utf8")}</style>`,
        `<defs>${RINGS.map(masksOf).join("")}</defs>`,
        RINGS.map(ringBody).join(""),
        "</svg>\n",
    ].join("");
}

function masksOf(ring: Ring): string {
    const width = ring.width + MASK_MARGIN;
    const end = `<path id="${ring.name}-end" d="${pinchedRing(ring.radius, width, END_TAPER_DEGREES)}" fill="#fff"/>`;
    return [
        `<mask id="${ring.name}-pocket" ${REGION}><path d="${pinchedRing(ring.radius, width, POCKET_DEGREES)}" fill="#fff"/></mask>`,
        `<mask id="${ring.name}-head" class="${ring.name}" ${REGION}><g class="head">${end}</g></mask>`,
        `<mask id="${ring.name}-tail" class="${ring.name}" ${REGION}><use href="#${ring.name}-end" class="tail"/></mask>`,
    ].join("");
}

function ringBody(ring: Ring): string {
    const body = [
        `<g class="spin ${ring.name}">`,
        `<g mask="url(#${ring.name}-pocket)"><g mask="url(#${ring.name}-head)"><g mask="url(#${ring.name}-tail)">`,
        `<path class="arc" pathLength="100" d="${circleFromTop(ring.radius)}" stroke="${ring.color}" stroke-width="${ring.width}"/>`,
        "</g></g></g></g>",
    ].join("");
    return ring.clockwise ? body : `<g transform="scale(-1 1)">${body}</g>`;
}

function pinchedRing(radius: number, width: number, span: number): string {
    const outer: Point[] = [];
    const inner: Point[] = [];
    for (let sample = 0; sample <= RING_SAMPLES; sample++) {
        const degrees = (360 * sample) / RING_SAMPLES;
        const halfWidth = (width * smoothstep(Math.min(degrees, 360 - degrees) / span)) / 2;
        outer.push(pointAt(radius + halfWidth, degrees));
        inner.push(pointAt(radius - halfWidth, degrees));
    }
    return `M${[...outer, ...inner.reverse()].map(formatPoint).join("L")}Z`;
}

function pointAt(radius: number, degrees: number): Point {
    const radians = ((degrees - 90) * Math.PI) / 180;
    return [radius * Math.cos(radians), radius * Math.sin(radians)];
}

function circleFromTop(radius: number): string {
    const half = `A${radius} ${radius} 0 1 1`;
    return `M0 ${-radius}${half} 0 ${radius}${half} 0 ${-radius}`;
}
