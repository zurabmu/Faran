<svelte:options customElement={{ tag: "faran-entry" }} />

<script lang="ts">
    import { prefersReducedMotion } from "svelte/motion";
    import { dropOnWater } from "@/water";
    import { Surfacing } from "@/entry/surfacing.svelte";

    const id = $props.id();
    const surfacing = new Surfacing((element) => {
        const { left, top, width, height } = element.getBoundingClientRect();
        dropOnWater({ x: left + width / 2, y: top + height / 2, strength: 6 });
    });
    const depth = $derived(prefersReducedMotion.current ? 0 : 1 - surfacing.progress);
</script>

<div class="entry" style:--depth={depth} {@attach (element) => surfacing.watch(element)}>
    <svg class="filters" aria-hidden="true">
        <filter id="{id}-water" x="-10%" y="-40%" width="120%" height="180%">
            <feTurbulence type="fractalNoise" baseFrequency="0.012 0.05" numOctaves="2" seed="7" result="ripples" />
            <feOffset in="ripples" result="moving">
                {#if !prefersReducedMotion.current}
                    <animate attributeName="dx" values="0;60;0" dur="9s" repeatCount="indefinite" />
                {/if}
            </feOffset>
            <feDisplacementMap in="SourceGraphic" in2="moving" scale={depth * 22} xChannelSelector="R" yChannelSelector="G" />
            <feGaussianBlur stdDeviation={depth * 2.4} />
        </filter>
    </svg>
    <div class="content" style:filter="url(#{id}-water)">
        <span class="headword"><b class="word">faran</b> <i class="part">Old English, verb</i></span>
        <span class="sense">
            To go, used of long distances, or to travel. Middle English kept it as <i>faren</i>, which survives in the modern word
            <i>fare</i>.
        </span>
        <a class="source" href="https://en.wiktionary.org/wiki/faran">Wiktionary</a>
    </div>
</div>

<style>
    .entry {
        position: relative;
        display: inline-block;
        max-width: 30rem;
        color: var(--faran-text-muted, #b8afc6);
        font-family: var(--faran-font-text, system-ui, sans-serif);
        font-size: 0.68rem;
        line-height: 1.5;
        text-align: center;
    }

    .filters {
        position: absolute;
        width: 0;
        height: 0;
    }

    .content {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.3rem;
        opacity: calc(1 - var(--depth));
        transform: scale(calc(1 - var(--depth) * 0.12));
    }

    .headword {
        display: flex;
        align-items: baseline;
        gap: 0.5em;
    }

    .word {
        color: var(--faran-text, #f1ecf4);
        font-size: 1.5em;
        font-weight: 600;
    }

    .source {
        margin-top: 0.2rem;
        color: var(--faran-text-muted, #b8afc6);
        font-size: 0.9em;
        text-decoration: none;
    }

    .source:is(:hover, :focus-visible) {
        color: var(--faran-end-text, #a3a6ff);
    }
</style>
