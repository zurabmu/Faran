<script lang="ts">
    import type { Animation } from "@engine/animation";
    import type { Playback } from "@engine/playback.svelte";
    import { cssColor } from "@engine/style";
    import Controls from "@engine/player/Controls.svelte";
    import Legend from "@engine/player/Legend.svelte";
    import SceneView from "@engine/player/SceneView.svelte";
    import SidePanel from "@engine/player/SidePanel.svelte";
    import { PlayerView } from "@engine/player/view.svelte";

    let { animation, playback, showsControls, legendOpen }: { animation: Animation; playback: Playback; showsControls: boolean; legendOpen: boolean } =
        $props();

    const view = new PlayerView(() => ({ animation, playback }));
</script>

<div class="player">
    <div class="animation" class:single-column={!view.hasSidePanel} style:background-color={cssColor(animation.backgroundColor)}>
        <div class="stage">
            <SceneView renderings={[...animation.background, ...view.frame.renderings]} bounds={view.bounds} />
            <Legend entries={animation.legend} open={legendOpen} />
        </div>
        {#if view.hasSidePanel}
            <SidePanel rows={view.frame.info} charts={animation.charts} step={playback.step} seek={(step) => playback.seek(step)} />
        {/if}
        {#if showsControls}
            <Controls {playback} />
        {/if}
    </div>
</div>

<style>
    .player {
        container: faran-animation / inline-size;
        width: 100%;
        height: 100%;
    }

    .player :global(*) {
        box-sizing: border-box;
    }

    .animation {
        --text: var(--faran-text, #f1ecf4);
        --muted: var(--faran-text-muted, #b8afc6);
        --faint: var(--faran-text-faint, #a59cb5);
        --rule: var(--faran-rule, #2b2636);
        --rule-strong: var(--faran-rule-strong, #3e3650);
        --surface: var(--faran-surface, #17141f);
        --accent: var(--faran-start-text, #ffa487);
        display: grid;
        grid-template-columns: minmax(0, 1fr) minmax(13rem, 17rem);
        grid-template-rows: minmax(0, 1fr) auto;
        width: 100%;
        height: 100%;
        min-height: 18rem;
        color: var(--text);
        font: 13px/1.45 var(--faran-font-text, "Source Sans 3", system-ui, sans-serif);
    }

    .animation.single-column {
        grid-template-columns: minmax(0, 1fr);
    }

    .stage {
        position: relative;
        min-width: 0;
        min-height: 0;
    }

    @container faran-animation (max-width: 40rem) {
        .animation {
            grid-template-columns: minmax(0, 1fr);
            grid-template-rows: minmax(14rem, 1fr) auto minmax(0, 8.5rem);
        }
    }
</style>
