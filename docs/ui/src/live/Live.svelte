<svelte:options
    customElement={{ tag: "faran-live", props: { caption: { type: "String" }, still: { type: "Boolean" } } }}
/>

<script lang="ts">
    import Failure from "@/shared/Failure.svelte";
    import { Hint, HintTour } from "@/shared/hint";
    import Loader from "@/shared/Loader.svelte";
    import { AnimationPlayer, Player } from "@/shared/player";
    import Animation from "@/live/Animation.svelte";
    import { LiveSession } from "@/live/session.svelte";
    import { sourceOf } from "@/live/source";
    import Start from "@/live/Start.svelte";

    let { caption, still = false }: { caption: string; still: boolean } = $props();

    const session = new LiveSession(sourceOf($host()));
    const player = new AnimationPlayer();
    const tour = new HintTour({ name: "live-preview-hint", texts: ["You can edit the code here.", "Then click here to run it."] });
</script>

<div class="anchor" {@attach (element) => tour.connect(element)}>
    <Player title={caption} {player} hasPlayback={!still} attachSourceButton={tour.target(0)}>
        {#snippet actions(sourceOpen)}
            <button type="button" disabled={session.running} onclick={() => session.run()} {@attach tour.target(1)}>Run code</button>
            {#if sourceOpen}
                <button type="button" disabled={!session.editable} onclick={() => session.reset()}>Reset code</button>
            {/if}
        {/snippet}
        <div class="live">
            <div class="player">
                {#if session.animation !== undefined}
                    <Animation animation={session.animation} {player} />
                {:else if !session.running}
                    <Start status={session.status} onstart={() => session.run()} />
                {/if}
                {#if session.running}
                    <Loader label={session.status} active={true} />
                {/if}
            </div>
            <Failure message={session.failure} />
        </div>
        {#snippet source()}
            <div class="editor" {@attach (element) => session.attachEditor(element)}></div>
        {/snippet}
    </Player>
    <Hint {tour} />
</div>

<style>
    :host {
        display: block;
        margin: 1.5rem 0 2rem;
    }

    .anchor {
        position: relative;
    }

    .live {
        display: flex;
        flex-direction: column;
    }

    .player {
        position: relative;
        flex: 1;
        display: grid;
        grid-template-rows: minmax(0, 1fr);
        min-height: 26rem;
    }

    :global(.expanded) .player {
        min-height: 0;
    }

    @media screen and (max-width: 44.984375em) {
        .player {
            min-height: 32rem;
        }
    }
</style>
