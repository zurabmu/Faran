<script lang="ts">
    import type { HTMLButtonAttributes } from "svelte/elements";
    import Icon from "@/shared/Icon.svelte";

    // svelte-ignore custom_element_props_identifier
    // The rest of the props carry attachments and button attributes onto the button.
    let { label, icon, ...attributes }: { label: string; icon: string } & Omit<HTMLButtonAttributes, "type" | "title" | "children"> = $props();
</script>

<button type="button" aria-label={label} title={label} {...attributes}><Icon path={icon} /></button>
