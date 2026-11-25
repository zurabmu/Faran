import { siteUrl } from "@/shared/site";

const BINDER = "https://mybinder.org/v2/gh/zurabmu/faran/main";

/**
 * The address of the replay page that shows `recording`, a file name in
 * `docs/content/visualizations/mpcc-simulation/` without `.frn`.
 */
export function replayPageUrl(recording: string): string {
    const page = siteUrl("viewer/index.html");
    page.searchParams.set("visualization", `../visualizations/mpcc-simulation/${recording}.frn`);
    return page.href;
}

/**
 * The address that opens `notebook`, a notebook name without `.ipynb`, on Binder.
 */
export function binderUrl(notebook: string): string {
    return `${BINDER}?filepath=notebooks/${notebook}.ipynb`;
}
