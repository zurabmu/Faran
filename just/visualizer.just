# Build the visualizer CLI that pytest --visualize runs
[working-directory("visualizer/core")]
build-visualizer:
    pnpm install --frozen-lockfile
    pnpm build
    git update-index --skip-worktree ../faran_visualizer/assets/cli.js
