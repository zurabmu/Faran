# Generate Jupyter notebooks from documentation examples
notebooks:
    uv run python -m tests.notebooks

# Build the Svelte components that the documentation pages use
docs-ui:
    cd docs/ui && pnpm install --frozen-lockfile && pnpm build

# Build the documentation site into site/
docs-build:
    uv run zensical build --clean --strict

# Serve the documentation site with live reload
docs-serve:
    uv run zensical serve

# Run the documentation examples and save their visualizations to docs/content/visualizations/
docs-examples:
    uv run pytest -m docs --visualize
