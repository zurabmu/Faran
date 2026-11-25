/**
 * The parts of a Pyodide runtime that the workers use.
 */
export interface Pyodide {
    loadPackage(names: string[]): Promise<void>;
    pyimport(name: string): { install(urls: string | string[]): Promise<void> };
    runPython(code: string): unknown;
    unpackArchive(buffer: ArrayBuffer, format: string): void;
    globals: { get(name: string): unknown };
}

/**
 * Where a worker finds the site's Python files, and where it sends status texts.
 */
export interface PythonOptions {
    readonly assetsUrl: string;
    readonly report: (status: string) => void;
}

interface Download {
    readonly title: string;
}

interface PyodidePackage extends Download {
    readonly name: string;
}

interface Wheel extends Download {
    readonly manifest: string;
}

const PYODIDE: Download = { title: "Pyodide" };
const PYODIDE_URL = "https://cdn.jsdelivr.net/pyodide/v314.0.8/full/";
const INSTALLER = "micropip";
const PACKAGES: readonly PyodidePackage[] = [
    { name: "numpy", title: "NumPy" },
    { name: "scipy", title: "SciPy" },
    { name: "msgspec", title: "msgspec" },
];
const FARAN: Wheel = { manifest: "faran-wheel.txt", title: "Faran" };
const WHEELS: readonly Wheel[] = [
    FARAN,
    { manifest: "visualizer-wheel.txt", title: "the Faran visualizer" },
];
const LAB_ARCHIVE = "lab.zip";
const WHEEL_COMMAND = "uv run python -m docs.scripts.wheel";

/**
 * A status text that names everything `startPython` downloads.
 */
export const FIRST_RUN_DOWNLOADS = `The first run downloads ${listed([PYODIDE, ...PACKAGES, ...WHEELS])}.`;

/**
 * Returns a function that loads the export `name` of the `lab` package. Its first call starts
 * Python in the current worker, and later calls return the same export.
 */
export function labExport<Exported>(name: string): (options: PythonOptions) => Promise<Exported> {
    let loaded: Promise<Exported> | undefined;
    return (options) => {
        loaded ??= importFromLab<Exported>(name, options);
        return loaded;
    };
}

async function importFromLab<Exported>(name: string, options: PythonOptions): Promise<Exported> {
    const pyodide = await startPython(options);
    options.report(`Importing ${FARAN.title}`);
    pyodide.runPython(`from lab import ${name}`);
    return pyodide.globals.get(name) as Exported;
}

/**
 * Starts Pyodide in the current worker with Faran and the `lab` package from `assetsUrl`, where
 * `docs/scripts/wheel.py` writes them.
 */
async function startPython({ assetsUrl, report }: PythonOptions): Promise<Pyodide> {
    const pyodide = await downloadPyodide(report);
    await loadPackages(pyodide, report);
    await installWheels(pyodide, { assetsUrl, report });
    await unpackLab(pyodide, assetsUrl);
    return pyodide;
}

async function downloadPyodide(report: (status: string) => void): Promise<Pyodide> {
    report(`Downloading ${PYODIDE.title}`);
    const { loadPyodide } = (await import(/* @vite-ignore */ `${PYODIDE_URL}pyodide.mjs`)) as {
        loadPyodide(options: { indexURL: string }): Promise<Pyodide>;
    };
    return loadPyodide({ indexURL: PYODIDE_URL });
}

async function loadPackages(pyodide: Pyodide, report: (status: string) => void): Promise<void> {
    report(`Loading ${listed(PACKAGES)}`);
    await pyodide.loadPackage([...PACKAGES.map(({ name }) => name), INSTALLER]);
}

async function installWheels(pyodide: Pyodide, { assetsUrl, report }: PythonOptions): Promise<void> {
    report(`Installing ${listed(WHEELS)}`);
    const urls = await Promise.all(WHEELS.map((wheel) => wheelUrl(assetsUrl, wheel)));
    await pyodide.pyimport(INSTALLER).install(urls);
}

async function unpackLab(pyodide: Pyodide, assetsUrl: string): Promise<void> {
    const archive = await fetchAsset(assetsUrl, LAB_ARCHIVE);
    pyodide.unpackArchive(await archive.arrayBuffer(), "zip");
}

async function wheelUrl(assetsUrl: string, { manifest }: Wheel): Promise<string> {
    const name = (await (await fetchAsset(assetsUrl, manifest)).text()).trim();
    return new URL(name, assetsUrl).href;
}

async function fetchAsset(assetsUrl: string, name: string): Promise<Response> {
    const url = new URL(name, assetsUrl);
    const response = await fetch(url);
    if (!response.ok) {
        throw new Error(`Expected ${url} to exist, but the server returned ${response.status}. Run "${WHEEL_COMMAND}" before building the site.`);
    }
    return response;
}

function listed(downloads: readonly Download[]): string {
    const titles = downloads.map(({ title }) => title);
    const last = titles.pop();
    if (last === undefined) throw new Error("Expected at least one download to list, but there are none.");
    return titles.length === 0 ? last : `${titles.join(", ")} and ${last}`;
}
