# Generate Jupyter notebooks from documentation examples
notebooks:
    uv run python -m tests.notebooks

# Build the documentation site into site/
docs-build:
    uv run zensical build --clean --strict

# Serve the documentation site with live reload
docs-serve:
    uv run zensical serve

# Run the documentation examples and save their visualizations to docs/visualizations/
docs-examples: build-visualizer
    uv run pytest -m docs --visualize
