<script lang="ts">
    import Loader from "@/shared/Loader.svelte";
    import { replayPageUrl } from "@/replay/addresses";
    import type { ReplayPlayer } from "@/replay/player.svelte";

    let { caption, recording, player }: { caption: string; recording: string; player: ReplayPlayer } = $props();
</script>

<div class="scene">
    <iframe src={replayPageUrl(recording)} title="Replay of the {caption.toLowerCase()} example" loading="lazy" {@attach (frame) => player.connect(frame)}></iframe>
    {#if !player.ready}
        <Loader label="Loading replay" active />
    {/if}
</div>

<style>
    .scene {
        position: relative;
        height: min(40rem, 80vh);
    }

    iframe {
        display: block;
        width: 100%;
        height: 100%;
        border: 0;
    }

    @media screen and (max-width: 44.984375em) {
        .scene {
            height: 75vh;
        }
    }
</style>
