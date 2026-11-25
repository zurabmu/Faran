<script lang="ts">
    import type { GallerySession } from "@/gallery/session.svelte";

    let { session }: { session: GallerySession } = $props();

    const LARGEST_DISPLACEMENT = 70;

    const filters = $derived([
        { id: "wash-away", amount: session.away },
        { id: "wash-forming", amount: session.forming },
    ]);
</script>

<svg aria-hidden="true">
    {#each filters as { id, amount } (id)}
        <filter {id} x="-10%" y="-10%" width="120%" height="120%">
            <feTurbulence type="fractalNoise" baseFrequency="0.006 0.03" numOctaves="2" />
            <feDisplacementMap in="SourceGraphic" xChannelSelector="R" yChannelSelector="G" scale={LARGEST_DISPLACEMENT * amount} />
        </filter>
    {/each}
</svg>

<style>
    svg {
        position: absolute;
        width: 0;
        height: 0;
    }
</style>
