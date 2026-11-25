# Generate Jupyter notebooks from documentation examples
notebooks:
    uv run python -m tests.notebooks

# Build the Faran wheel and the demo package that the home page lab loads in Pyodide
docs-wheel: visualizer-engine
    uv run python -m docs.scripts.wheel

# Build the Svelte components that the documentation pages use
docs-ui:
    cd docs/ui && pnpm install --frozen-lockfile && pnpm build

# Build the documentation site into site/
[parallel]
docs-build: docs-examples docs-wheel docs-ui
    uv run zensical build --clean --strict

# Build everything the documentation site needs and serve it with live reload
[parallel]
docs-serve: docs-examples docs-wheel docs-ui
    uv run zensical serve

# Serve the documentation site without running the documentation examples, so the example replays are the ones from the last run
[parallel]
docs-serve-quick: docs-wheel docs-ui
    uv run zensical serve

# Build everything the documentation site needs, serve it, and rebuild what a change to a source of the site affects
[parallel]
docs-watch: docs-examples docs-wheel docs-ui
    uv run python -m docs.scripts.watch

# Run the documentation examples and save their visualizations to docs/content/visualizations/
docs-examples:
    uv run pytest -m docs --visualize
