<svelte:options customElement={{ tag: "faran-gallery" }} />

<script lang="ts">
    import { dropOnColumnsOf } from "@/gallery/ripples";
    import { GallerySession } from "@/gallery/session.svelte";
    import { Tabs } from "@/shared/tabs.svelte";
    import { sectionOf, tabsOf } from "@/gallery/sections";
    import WashFilters from "@/gallery/WashFilters.svelte";

    const element = $host();
    const names = tabsOf(element);
    const session = new GallerySession(names.length, (index) => dropOnColumnsOf(sectionOf(element, index)));
    const id = $props.id();
    const tabs = new Tabs({ id, value: () => String(session.shown), choose: (value) => session.show(Number(value)) });

    $effect(() => session.start());
</script>

<div class="gallery" {...tabs.api.getRootProps()} {@attach tabs.root.attach} {@attach session.holdWhileEngaged}>
    <div class="tabs" {...tabs.api.getListProps()}>
        {#each names as name, index (index)}
            <button {...tabs.triggerProps(String(index))}>{name}</button>
        {/each}
    </div>
    <div class="panels">
        {#each names as name, index (index)}
            <div
                class="panel"
                class:visible={session.isVisible(index)}
                {...tabs.contentProps(String(index))}
                hidden={false}
                aria-label={name}
                inert={index !== session.shown}
                style:filter={session.filterOf(index)}
                style:opacity={1 - session.washOf(index)}
            >
                <svelte:element this={"slot"} name="panel-{index}" />
            </div>
        {/each}
    </div>
    <WashFilters {session} />
</div>

<style>
    :host {
        display: block;
        margin: 1.4rem 0 2.6rem;
    }

    .tabs {
        display: flex;
        flex-wrap: wrap;
        gap: 0.2rem 1.8rem;
        margin-bottom: 2rem;
        border-bottom: 1px solid var(--faran-rule, #2b2636);
    }

    button {
        position: relative;
        padding: 0.55rem 0;
        border: none;
        background: none;
        color: var(--faran-text-muted, #c9c0d4);
        cursor: pointer;
        font: inherit;
        font-size: 0.8rem;
        font-weight: 600;
        transition: color 0.15s;
    }

    button:is(:hover, :focus-visible, [aria-selected="true"]) {
        color: var(--faran-text, #f1ecf4);
    }

    button[aria-selected="true"]::after {
        content: "";
        position: absolute;
        right: 0;
        bottom: -1px;
        left: 0;
        height: 2px;
        background-color: var(--faran-start-text, #ffa487);
    }

    .panels {
        display: grid;
    }

    .panel {
        grid-area: 1 / 1;
        visibility: hidden;
    }

    .panel.visible {
        visibility: visible;
    }

    @media (prefers-reduced-motion: reduce) {
        button {
            transition: none;
        }
    }
</style>
