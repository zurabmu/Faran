# Writing the documentation

This guide is for you if you want to change a page of the documentation site, add a new one, or change how the site looks or behaves.

## See your changes

Run `just docs-watch` and open `http://127.0.0.1:8000/faran/`. It builds the site, serves it, and rebuilds whatever your change affects, so you can keep it running while you work. If a change doesn't show up, check [`scripts/watch/project.py`](scripts/watch/project.py), which lists the steps that run for each kind of file.

`just docs-serve` and `just docs-serve-quick` start faster, but they only reload Markdown. When you change anything in [`ui/`](ui/), [`extensions/`](extensions/), [`examples/`](examples/), [`faran/`](../faran/) or [`visualizer/`](../visualizer/), restart them. [`just/docs.just`](../just/docs.just) defines all three commands.

## Find the file behind a page

Take the path of the page's URL after `/faran/` and look under [`content/`](content/). For example, `http://127.0.0.1:8000/faran/guide/getting-started/` comes from [`content/guide/getting-started.md`](content/guide/getting-started.md). To add a page or move it in the navigation, edit the `nav` list in [`zensical.toml`](../zensical.toml).

## Use more than plain Markdown

Besides plain Markdown, you can use the extensions that [`zensical.toml`](../zensical.toml) enables, and the syntax that this project adds. Each module below explains its syntax in the docstring at the top of its block class, with an example you can copy:

- `/// backends` shows the NumPy and JAX versions of a class with a tab for each: [`extensions/backends.py`](extensions/backends.py)
- `[@key]` cites a paper, and `\bibliography` lists the cited papers: [`extensions/citations.py`](extensions/citations.py)
- `/// columns` puts two parts side by side: [`extensions/columns.py`](extensions/columns.py)
- `/// docs-map` draws a list of pages as a map: [`extensions/docsmap.py`](extensions/docsmap.py)
- `/// equation` numbers a formula and explains its symbols: [`extensions/equation.py`](extensions/equation.py)
- `/// features` lists the features from [`features.yaml`](features.yaml): [`extensions/features.py`](extensions/features.py)
- `/// gallery` shows one section at a time, with a tab for each: [`extensions/gallery.py`](extensions/gallery.py)
- `/// hero` is the header at the top of a page, as on the home page: [`extensions/hero.py`](extensions/hero.py)
- `/// live` runs a code snippet in the browser: [`extensions/live.py`](extensions/live.py)
- `/// replay` plays back a recorded example run: [`extensions/replay.py`](extensions/replay.py)
- `/// variants` shows one variant of some content at a time: [`extensions/variants.py`](extensions/variants.py)

## Show code

If the reader only needs to read the code, a plain code block is enough. The site dims the import lines at the top of a Python code block. If the imports are what you want to show, add the `faran-imports-shown` class to the block.

If the reader should try the code, write a live snippet. Put the script in [`snippets/`](snippets/). The docstring of `run_snippet` in [`lab/snippet.py`](lab/snippet.py) says what the script has to do so that it runs in the browser.

If you want to show a whole example run, use a replay. The examples are in [`examples/`](examples/). After you change one, run `just docs-examples` to record it again. The recording is saved in [`content/visualizations/`](content/visualizations/), named after the example's `SEED`, and that name is what the replay block takes.

## Document the API

Write parameters, fields, attributes and defaults in the docstrings, as the [Docstrings](../DESIGN.md#docstrings) section of the design guide describes. A `:::` block on a page renders them, so link to that section instead of repeating it in your text.

If readers shouldn't set a field of a dataclass, start its name with an underscore. [`extensions/signatures.py`](extensions/signatures.py) then leaves it out of the constructor signature.

## Write equations and cite papers

Put every display formula in a `/// equation` block, and refer to it with a link such as `equation [](#equation-mpc)`. Don't write "below", "above" or "the following".

Write a norm as `\lVert \mathbf{p} \rVert`, not `\|\mathbf{p}\|`. KaTeX joins `\|` with the symbol next to it, and the equation can then no longer highlight that symbol when the reader points at it in the legend.

To cite a paper, add its BibTeX entry to [`references.bib`](references.bib).

## Change how the site looks or behaves

Find the part you want to change:

- The Python extensions in [`extensions/`](extensions/) turn the Markdown into HTML.
- The Svelte components in [`ui/src/`](ui/src/), one folder each, make that HTML interactive. Each component holds its own styles. [`ui/src/index.ts`](ui/src/index.ts) imports all of them.
- The stylesheets in [`content/stylesheets/`](content/stylesheets/) style the rest of the page. [`loading.css`](content/stylesheets/loading.css) hides the page content until the component script has run, so readers never see a component before it's ready. While the content is hidden, it shows the spinner that [`ui/src/loading/spinner.ts`](ui/src/loading/spinner.ts) draws.
- The templates in [`overrides/`](overrides/) change the page layout of the Zensical theme.

## Add your own block

Write a module in [`extensions/`](extensions/) with a block class and a `makeExtension` function, and add the module to `markdown_extensions` in [`zensical.toml`](../zensical.toml). If your block needs to be interactive, give its element a tag of its own, and write a Svelte component for that tag in a new folder under [`ui/src/`](ui/src/), and import it in [`ui/src/index.ts`](ui/src/index.ts).

## Check your changes

- `just docs-build` builds the whole site and fails on any warning, such as a broken link.
- `uv run pytest tests/test_documentation` runs the tests in [`tests/test_documentation/`](../tests/test_documentation/).
- `uv run pytest -m docs` runs every snippet and example.
- `pnpm build` in [`ui/`](ui/) checks the components with svelte-check before it builds them.

## Don't edit generated files

The files listed in [`.gitignore`](../.gitignore) are generated, and the commands in [`just/docs.just`](../just/docs.just) overwrite them. Edit the files they're generated from.
