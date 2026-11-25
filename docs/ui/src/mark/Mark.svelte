<svelte:options customElement={{ tag: "faran-mark", props: { animate: { type: "Boolean" }, loading: { type: "Boolean" }, label: { type: "String" } } }} />

<script lang="ts">
    import { markDrawing } from "@/mark/drawing";
    import { dropAtMarkPoint } from "@/mark/splash";

    let { animate = false, loading = false, label = "Faran" }: { animate: boolean; loading: boolean; label: string } = $props();

    const revealed = $derived(animate || loading);

    const id = $props.id();
    const drawing = markDrawing();
</script>

<svg viewBox={drawing.viewBox} role="img" aria-label={label} class:animate class:loading>
    {#if revealed}
        <defs>
            {#each drawing.bodies as body, index (index)}
                <mask id="{id}-reveal-{index}" maskUnits="userSpaceOnUse" x="-200" y="-200" width="400" height="400">
                    <path
                        class="reveal"
                        d={body.centerline}
                        style:--length={body.length}
                        style:--delay="{0.15 + index * 0.85}s"
                        style:--loop-delay="{index * 0.45}s"
                        onanimationend={(event) => dropAtMarkPoint(event.currentTarget, body.end)}
                    />
                </mask>
            {/each}
        </defs>
    {/if}
    {#each drawing.bodies as body, index (index)}
        <path d={body.outline} fill={body.color} mask={revealed ? `url(#${id}-reveal-${index})` : undefined} />
    {/each}
</svg>

<style>
    :host {
        display: inline-block;
    }

    svg {
        display: block;
        width: 100%;
        height: auto;
        overflow: visible;
    }

    .reveal {
        fill: none;
        stroke: white;
        stroke-width: 20;
        stroke-dasharray: var(--length);
        stroke-dashoffset: 0;
    }

    .animate .reveal {
        animation: draw 0.85s cubic-bezier(0.45, 0, 0.25, 1) var(--delay) both;
    }

    .loading .reveal {
        animation: loop 2.6s cubic-bezier(0.45, 0, 0.25, 1) var(--loop-delay) infinite both;
    }

    @keyframes loop {
        0% {
            stroke-dashoffset: var(--length);
        }

        38%,
        66% {
            stroke-dashoffset: 0;
        }

        100% {
            stroke-dashoffset: var(--length);
        }
    }

    @keyframes draw {
        from {
            stroke-dashoffset: var(--length);
        }

        to {
            stroke-dashoffset: 0;
        }
    }

    @media (prefers-reduced-motion: reduce) {
        .animate .reveal,
        .loading .reveal {
            animation: none;
        }
    }
</style>
