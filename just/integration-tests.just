# Run integration tests: just integration-tests [list | visualize] [<pytest -k expression>]
integration-tests command="" test="": (_integration-tests (if command =~ '^(list|visualize)$' { command } else { "run" }) (if command =~ '^(list|visualize)$' { test } else { command }))

[private]
_integration-tests mode filter: (_pytest-integration ((if mode == "list" { "--collect-only -q" } else if mode == "visualize" { "--visualize" } else { "" }) + (if filter == "" { "" } else { " -k " + quote(filter) })))

# PYTEST_ADDOPTS carries the -k expression because cmd mangles double quotes in recipe lines.
[private]
_pytest-integration $PYTEST_ADDOPTS:
    uv run pytest -m integration
