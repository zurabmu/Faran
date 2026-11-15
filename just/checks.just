default_modules := ". visualizer"

[unix]
check modules=default_modules:
    for dir in {{modules}}; do \
        echo "=== Checking $dir ===" && \
        pushd "$dir" && \
        source .venv/bin/activate && \
        ruff check --fix && \
        ruff format && \
        pyright && \
        pytest && \
        popd; \
    done

[windows]
check modules=default_modules:
    for %d in ({{modules}}) do @echo === Checking %d === && pushd %d && .venv\Scripts\activate.bat && ruff check --fix && ruff format && pyright && pytest && popd
