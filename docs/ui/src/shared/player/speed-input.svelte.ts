import * as numberInput from "@zag-js/number-input";
import { normalizeProps, useMachine } from "@zag-js/svelte";
import { RootNode } from "@/shared/dom/root";

const SLOWEST = 0.1;
const FASTEST = 10;
const INCREMENT = 0.05;
const FORMAT: Intl.NumberFormatOptions = { minimumFractionDigits: 2, maximumFractionDigits: 2 };

/**
 * A number input for the playback speed, as a multiple of real time, that can also be scrubbed
 * by dragging its label. Create it while a component initializes.
 */
export class SpeedInput {
    readonly root = new RootNode();
    readonly api: numberInput.Api;

    constructor({ id, speed, disabled, onchange }: { id: string; speed: () => number; disabled: () => boolean; onchange: (speed: number) => void }) {
        const service = useMachine(numberInput.machine, () => ({
            id,
            getRootNode: this.root.get,
            defaultValue: String(speed()),
            min: SLOWEST,
            max: FASTEST,
            step: INCREMENT,
            disabled: disabled(),
            formatOptions: FORMAT,
            onValueChange: ({ valueAsNumber }: numberInput.ValueChangeDetails) => {
                const isSpeed = valueAsNumber > 0;
                if (isSpeed) onchange(valueAsNumber);
            },
        }));
        this.api = $derived(numberInput.connect(service, normalizeProps));
    }

    /**
     * Keeps a press on the field from starting a scrub while the reader types in it.
     */
    keepTyping(event: MouseEvent): void {
        if (this.api.focused) event.stopPropagation();
    }
}
