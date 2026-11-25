<svelte:options
    customElement={{
        tag: "faran-replay",
        props: { caption: { type: "String" }, recording: { type: "String" }, notebook: { type: "String" } },
    }}
/>

<script lang="ts">
    import { Player } from "@/shared/player";
    import { binderUrl } from "@/replay/addresses";
    import { ReplayPlayer } from "@/replay/player.svelte";
    import Scene from "@/replay/Scene.svelte";

    let { caption, recording, notebook }: { caption: string; recording: string; notebook: string } = $props();

    const player = new ReplayPlayer();
</script>

<Player title={caption} {player} hasPlayback={true} attachSourceButton={() => {}}>
    {#snippet actions()}
        <button type="button" disabled={!player.ready} onclick={() => player.resetLayout()}>Reset layout</button>
        <a href={binderUrl(notebook)}>Run on Binder</a>
    {/snippet}
    <Scene {caption} {recording} {player} />
    {#snippet source()}
        <slot name="source" />
    {/snippet}
</Player>

<style>
    :host {
        display: block;
        margin: 1.6em 0;
    }
</style>
