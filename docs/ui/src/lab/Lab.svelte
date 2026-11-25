<svelte:options customElement={{ tag: "faran-lab" }} />

<script lang="ts">
    import Actions from "@/shared/Actions.svelte";
    import Failure from "@/shared/Failure.svelte";
    import { Bar, Frame, Title, View } from "@/shared/frame";
    import Loader from "@/shared/Loader.svelte";
    import { SceneView } from "@/shared/scene";
    import DemoButtons from "@/lab/DemoButtons.svelte";
    import Readout from "@/lab/Readout.svelte";
    import { LabSession } from "@/lab/session.svelte";

    const PADDING = 24;

    const session = new LabSession();
</script>

<Frame title="Faran lab">
    <View>
        <div class="view">
            {#if session.isDrawable}
                <SceneView renderings={session.renderings} bounds={session.bounds} padding={PADDING} />
            {:else}
                <Loader label={session.running ? "Starting Python" : "Press Run to start"} active={session.running} />
            {/if}
        </div>
        <Failure message={session.failure} />
    </View>
    <Bar edge="bottom">
        <Title text="Faran lab" />
        <Actions><DemoButtons {session} /></Actions>
        <Readout status={session.status} entries={session.readout} />
    </Bar>
</Frame>

<style>
    :host {
        display: block;
        margin: 0 0 2.5rem;
    }

    .view {
        position: relative;
        aspect-ratio: 16 / 8;
    }

    @media screen and (max-width: 44.984375em) {
        .view {
            aspect-ratio: 4 / 3;
        }
    }
</style>
