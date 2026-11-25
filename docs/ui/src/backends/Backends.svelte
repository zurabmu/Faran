<svelte:options customElement={{ tag: "faran-backends" }} />

<script lang="ts">
    import { showLinkedSlots } from "@/shared/dom/linked";
    import { Tabs } from "@/shared/tabs.svelte";
    import { BACKENDS, backendChoice } from "@/backends/choice.svelte";

    const element = $host();
    const id = $props.id();
    const tabs = new Tabs({ id, value: () => backendChoice.backend, choose: (name) => backendChoice.choose(name) });

    $effect(() => showLinkedSlots(element, (slot) => backendChoice.chooseSlot(slot)));
</script>

<div {...tabs.api.getRootProps()} {@attach tabs.root.attach}>
    <div class="tabs" {...tabs.api.getListProps()}>
        {#each BACKENDS as backend (backend)}
            <button type="button" {...tabs.triggerProps(backend)}>{backend}</button>
        {/each}
    </div>
    <div {...tabs.contentProps(backendChoice.backend)}>
        <svelte:element this={"slot"} name={backendChoice.backend} />
    </div>
</div>

<style>
    :host {
        display: block;
        margin: 2rem 0;
    }

    .tabs {
        display: flex;
    }

    button {
        margin-bottom: -1px;
        padding: 0.35rem 0.9rem;
        border: 1px solid transparent;
        border-bottom: none;
        background: none;
        color: var(--faran-text-muted, #c9c0d4);
        cursor: pointer;
        font: inherit;
        font-size: 0.72rem;
        font-weight: 600;
    }

    button:is(:hover, :focus-visible) {
        color: var(--faran-text, #f1ecf4);
    }

    button[aria-selected="true"] {
        position: relative;
        border-color: var(--faran-rule, #2b2636);
        background-color: var(--faran-surface, #17141f);
        color: var(--faran-text, #f1ecf4);
        box-shadow: inset 0 2px 0 var(--faran-start-text, #ffa487);
    }
</style>
