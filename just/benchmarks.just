# Run benchmarks and save to JSON
bench:
    uv run pytest -m benchmark --benchmark-json=benchmark.json -v

# Run benchmarks and save as baseline
bench-baseline:
    uv run pytest -m benchmark --benchmark-autosave -v

# Run risk metric benchmarks and save to JSON
bench-risk *args:
    uv run pytest -m risk_benchmark --benchmark-json=benchmark_risk.json -v -s {{ args }}

# Generate report for benchmark results
bench-report *args:
    uv run python -m tests.benchmarks.report {{ args }}

# Generate report for risk metric benchmark results
bench-risk-report *args:
    uv run python -m tests.benchmarks.report show benchmark_risk.json {{ args }}

# Run benchmarks then generate report
bench-and-report *args: bench
    uv run python -m tests.benchmarks.report show benchmark.json {{ args }}

# Run risk metric benchmarks then generate report
bench-risk-and-report bench_flags="" *args:
    just bench-risk {{ bench_flags }}
    uv run python -m tests.benchmarks.report show benchmark_risk.json {{ args }}
