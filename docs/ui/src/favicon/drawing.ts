import { piece, stroke } from "@/geometry";
import { brand } from "@/shared/brand";

const STROKE = 3.4;
const STEM_X = 14.1;
const HOOK_RADIUS = 6;
const HOOK_CENTER_Y = 10.7;
const HOOK_END_DEGREES = 320;
const TURN_RADIUS = 2.2;
const ARM_Y = 16.4;
const ARM_END_X = 8.4;

function hookPath(): string {
    return stroke([
        piece.arc([STEM_X + HOOK_RADIUS, HOOK_CENTER_Y], HOOK_RADIUS, HOOK_END_DEGREES, 180),
        piece.line([STEM_X, HOOK_CENTER_Y], [STEM_X, ARM_Y - TURN_RADIUS]),
        piece.arc([STEM_X - TURN_RADIUS, ARM_Y - TURN_RADIUS], TURN_RADIUS, 0, 90),
        piece.line([STEM_X - TURN_RADIUS, ARM_Y], [ARM_END_X, ARM_Y]),
    ]).pathData();
}

export function faviconSvg({ tile }: { tile: boolean }): string {
    const hook = hookPath();
    const ground = tile ? `<rect width="32" height="32" rx="7" fill="${brand.tile}"/>` : "";
    return [
        `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" role="img" aria-label="Faran"><title>Faran</title>${ground}`,
        `<g fill="none" stroke-width="${STROKE}" stroke-linecap="round" stroke-linejoin="round">`,
        `<path d="${hook}" stroke="${brand.taken}"/>`,
        `<path d="${hook}" stroke="${brand.plan}" transform="rotate(180 16 16)"/>`,
        "</g></svg>\n",
    ].join("");
}
