const bundleUrl = import.meta.url;

/**
 * Resolves a path against the root of the documentation site, so that a component finds
 * site files from any page.
 */
export function siteUrl(path: string): URL {
    return new URL(`../../${path}`, bundleUrl);
}

/**
 * The address of the site's Python files, which `docs/scripts/wheel.py` writes, for a worker
 * that starts Python.
 */
export function pythonAssetsUrl(): string {
    return siteUrl("assets/pyodide/").href;
}
