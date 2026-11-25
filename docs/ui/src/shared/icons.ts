/**
 * Stroke paths of the control icons, drawn by `Icon.svelte` in a 16 by 16 view box.
 */
export const icons = {
    play: "M5 3.2v9.6L12.6 8z",
    pause: "M5.5 3.5v9M10.5 3.5v9",
    toStart: "M3.5 3.5v9M13 4 8.5 8l4.5 4zM8.5 4 4 8l4.5 4z",
    stepBack: "M11.5 3.5v9M9 4 4.5 8 9 12z",
    stepForward: "M4.5 3.5v9M7 4l4.5 4L7 12z",
    chevron: "M4.5 6.5 8 10l3.5-3.5",
    stop: "M4.2 4.2h7.6v7.6H4.2z",
    code: "M5.5 4.5 2 8l3.5 3.5M10.5 4.5 14 8l-3.5 3.5",
    copy: "M5.5 5.5h7v7h-7zM10.5 5.5v-2h-7v7h2",
    check: "M3 8.5l3 3 7-7",
    expand: "M2.5 6V2.5H6M10 2.5h3.5V6M13.5 10v3.5H10M6 13.5H2.5V10",
    collapse: "M6 2.5V6H2.5M10 2.5V6h3.5M13.5 10H10v3.5M2.5 10H6v3.5",
    reset: "M2.8 2.8v3.4h3.4M3.2 6.2A5.2 5.2 0 1 1 2.9 9.4",
} as const;
