export type Backend = "numpy" | "jax" | "cuda";

/**
 * The backends a reader can install.
 */
export const backends = [
    { value: "numpy", label: "NumPy", note: "CPU, no extra" },
    { value: "jax", label: "JAX", note: "CPU" },
    { value: "cuda", label: "JAX with CUDA", note: "NVIDIA GPU, Linux" },
] as const satisfies readonly { value: Backend; label: string; note: string }[];

const REQUIREMENTS: Record<Backend, string> = { numpy: "faran", jax: "faran[jax]", cuda: "faran[cuda]" };

/**
 * Builds the pip command for a backend, with the visualizer package added when asked for.
 */
export function installCommand({ backend, visualizer }: { backend: Backend; visualizer: boolean }): string {
    return ["pip install", REQUIREMENTS[backend], ...(visualizer ? ["faran-visualizer"] : [])].join(" ");
}
