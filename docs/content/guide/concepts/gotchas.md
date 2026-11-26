---
status: draft
---

# Gotchas

Known limitations and behaviors that are easy to miss. If you hit something not listed here, please [open an issue](https://gitlab.com/risk-metrics/faran/-/issues).

## JAX Is Not Installed by Default

`pip install faran` installs the NumPy backend only. Importing from `faran.jax` without JAX installed raises `ModuleNotFoundError`.

**Workaround:** Install `faran[jax]`, or `faran[cuda]` for GPU support. See [Backends](../backends.md).

## The First JAX Planner Step Is Slow

The JAX backend compiles a planner step the first time it runs, so the first call takes much longer than the calls after it. JAX compiles again whenever the shapes of the arrays change, for example when you change the number of rollouts or the horizon.

**Workaround:** Keep array shapes fixed between steps, and leave the first step out when you measure how long a step takes.

## A Compiled Function Must Receive Every Component It Uses

A function that you compile with `nnx.jit` raises `UntracedStateError` when it reads a component that it does not receive as an argument, for example one it reads through a closure.

**Workaround:** Register the component with `register` and pass it to the compiled function as an argument. See [Compiling Your Own Functions](../backends.md#compiling-your-own-functions).

## JAX Computes in 32-bit Floats by Default

JAX uses 32-bit floats unless 64-bit floats are enabled, while NumPy uses 64-bit floats. The two backends can therefore give slightly different results for the same inputs.

**Workaround:** Enable 64-bit floats with `jax.config.update("jax_enable_x64", True)` before you create any components, if you need the same precision as the NumPy backend.

## The Number of Obstacles Is Fixed

An obstacle state history has a fixed obstacle count, which you choose when you create it. An obstacle that is not observed at a time step has `NaN` as its state. Distance functions treat such an obstacle as infinitely far away, so it adds no collision cost.

**Workaround:** Create the history with the largest number of obstacles you expect, and leave the states of the obstacles that are not present as `NaN`.

## No Planner Uses Gradients

Faran has no gradient-based planner, and gradients of the JAX cost functions are not tested. Some of them, for example the collision costs, may not have useful gradients for `jax.grad`.

**Workaround:** Use the sampling-based [MPPI planner](../../api/mppi/index.md#mppi), which does not need gradients.

## SAT Distance Is Two-Dimensional and Uses One Ego Polygon

The SAT distance (`distance.sat`) works with convex polygons in the plane only, placed by their x and y positions and their headings. The ego vehicle is described by a single polygon.

**Workaround:** None for now. You can open [a feature request](https://gitlab.com/risk-metrics/faran/-/issues).
