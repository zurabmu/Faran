import * as radioGroup from "@zag-js/radio-group";
import { normalizeProps, useMachine } from "@zag-js/svelte";
import { RootNode } from "@/shared/dom/root";

/**
 * One option of a choice. `note` is a short description, or an empty string for none.
 */
export interface ChoiceOption<Value extends string> {
    readonly value: Value;
    readonly label: string;
    readonly note: string;
}

/**
 * An accessible radio group over `options`, which shows `value` and calls `choose` with the
 * option the reader picks. Create it while a component initializes.
 */
export class RadioChoice<Value extends string> {
    readonly root = new RootNode();
    readonly api: radioGroup.Api;

    constructor({
        id,
        options,
        value,
        choose,
    }: {
        id: string;
        options: () => readonly ChoiceOption<Value>[];
        value: () => Value;
        choose: (value: Value) => void;
    }) {
        const service = useMachine(radioGroup.machine, () => ({
            id,
            getRootNode: this.root.get,
            value: value(),
            onValueChange: ({ value: picked }: radioGroup.ValueChangeDetails) => choose(optionOf(options(), picked).value),
        }));
        this.api = $derived(radioGroup.connect(service, normalizeProps));
    }
}

function optionOf<Value extends string>(options: readonly ChoiceOption<Value>[], picked: string | null): ChoiceOption<Value> {
    const option = options.find((candidate) => candidate.value === picked);
    if (option === undefined) throw new Error(`Expected the picked value "${picked}" to be one of ${options.map(({ value }) => value).join(", ")}, but it is not.`);
    return option;
}
