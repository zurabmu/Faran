export const BACKENDS = ["NumPy", "JAX"] as const;

export type Backend = (typeof BACKENDS)[number];

/**
 * The backend that every `<faran-backends>` element and the backend switch of the table of
 * contents show. It starts at NumPy.
 */
class BackendChoice {
    backend = $state<Backend>("NumPy");

    /**
     * Chooses the backend whose part of a `<faran-backends>` element is in `slot`, when one is.
     * Returns whether it chose one.
     */
    chooseSlot(slot: string): boolean {
        const backend = backendNamed(slot);
        if (backend === undefined) return false;
        this.backend = backend;
        return true;
    }

    /**
     * Chooses the backend called `name`, which must be one of the backends.
     */
    choose(name: string): void {
        const backend = backendNamed(name);
        if (backend === undefined) throw new Error(`Expected "${name}" to be one of the backends ${BACKENDS.join(", ")}, but it is not.`);
        this.backend = backend;
    }
}

export const backendChoice = new BackendChoice();

function backendNamed(name: string): Backend | undefined {
    return BACKENDS.find((backend) => backend === name);
}
