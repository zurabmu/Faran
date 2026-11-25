import { normalizeProps, useMachine } from "@zag-js/svelte";
import * as tabs from "@zag-js/tabs";
import { RootNode } from "@/shared/dom/root";

/**
 * Accessible tabs that show the tab named by `value` and call `choose` with the tab the reader
 * picks, so the shown tab lives outside the component. Create it while a component initializes.
 */
export class Tabs {
    readonly root = new RootNode();
    readonly api: tabs.Api;

    constructor({ id, value, choose }: { id: string; value: () => string; choose: (value: string) => void }) {
        const service = useMachine(tabs.machine, () => ({
            id,
            getRootNode: this.root.get,
            value: value(),
            onValueChange: ({ value: picked }: tabs.ValueChangeDetails) => choose(picked),
        }));
        this.api = $derived(tabs.connect(service, normalizeProps));
    }

    triggerProps(value: string) {
        return this.api.getTriggerProps({ value });
    }

    contentProps(value: string) {
        return this.api.getContentProps({ value });
    }
}
