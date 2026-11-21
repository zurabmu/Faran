# Contributing to Faran

Hi! Thanks for considering contributing to Faran. All contributions are welcome, from typo fixes to architectural changes. Here's a quick guide to get you started, but feel free to reach out if you have any questions or need help.

## Development Setup

### Prerequisites

- Python ≥ 3.13
- [uv](https://github.com/astral-sh/uv) (recommended) or pip
- [just](https://github.com/casey/just) (optional, for convenience)

### Getting Started

1. Clone the repository:
   ```bash
   git clone https://gitlab.com/risk-metrics/faran.git
   cd faran
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   uv sync
   ```

   This installs all dependency groups by default. See the [uv documentation](https://docs.astral.sh/uv/getting-started/installation/) to install uv if you haven't already.

3. (Optional) Install pre-commit hooks:
   ```bash
   uv run pre-commit install
   ```

   These will run some checks for you before each commit, but you can also run them manually later.

## The Quick Guide

1. Create a branch from `main` with a [descriptive name](#branch-naming-convention).
2. Make your changes following the [design guide](DESIGN.md).
3. Add tests for any new functionality.
4. Run the full check suite:
    - `just check` (recommended), or
    - `uv run ruff check --fix && uv run ruff format && uv run pyright && uv run pytest` (manually).
5. Update documentation if needed.
6. Submit a merge request with a clear description.
7. Open an issue if you have any questions or need help.

## Branch Naming Convention

Depending on the type of work, use the following format for branch names:
- **Feature**: `feature/<short-description>`
- **Bugfix**: `bugfix/<short-description>`
- **Refactor**: `refactor/<short-description>`
- **Performance**: `performance/<short-description>`
- **Documentation**: `docs/<short-description>`
- **Tests**: `tests/<short-description>`
- **Chore**: `chore/<short-description>`
- **Other**: `other/<short-description>`

## Running Things

### Linting & Formatting

```bash
uv run ruff check --fix
uv run ruff format
```

### Type Checking

```bash
uv run pyright
```

### Tests

```bash
# Run unit tests
uv run pytest

# Run with coverage
uv run pytest --cov=faran --cov-report=term-missing

# Run specific test
uv run pytest tests/test_mppi.py -k "test_that_mppi_favors"

# Run documentation examples
uv run pytest -m docs  # --visualize will generate visualizations

# Run benchmarks
uv run pytest -m benchmark --benchmark-json=benchmark.json
```

### Integration Tests

```bash
just integration-tests <test>                   # Run integration tests
just integration-tests list <test>              # List integration tests
just integration-tests visualize <test>         # Run integration tests and generate visualizations of each
```

You can filter tests by specifying the optional `<test>` argument, which can be any [expression you would pass to the pytest `-k` option](https://docs.pytest.org/en/stable/example/markers.html#keyword-expressions). For example, `"test_that_planner_avoids_pedestrians[configuration1-jax-unicycle-pedestrian]"`, `pedestrian`, or `three_laps or pedestrian`. Quote the expression when it contains brackets or spaces.

The generated visualizations are saved under `tests/visualizations/` as recordings (`.frn` files). You can view a visualization in the viewer by running `just view <files>`, or in the browser by running `just view <files> --browser`.

If you don't have `just`, run the following commands:

```bash
uv run pytest -m integration -k <test>               # Run integration tests
uv run pytest -m integration -k <test> --visualize   # Run integration tests and generate visualizations
```

### Documentation

```bash
just docs-serve
```

Visit `http://127.0.0.1:8000/faran/` to preview.

## Further Reading

For our code style, testing philosophy, and design conventions, see the [Design Guide](DESIGN.md).
