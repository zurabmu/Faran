# Build the canvas engine that the canvas renderer and the documentation draw with
visualizer-engine:
    cd visualizer/engine && pnpm install --frozen-lockfile && pnpm build

# Open visualizations in the viewer of their renderer: just view <files> [--browser]
view +recordings:
    uv run faran-visualizer view {{recordings}}
