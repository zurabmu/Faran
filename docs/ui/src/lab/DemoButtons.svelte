<script lang="ts">
    import IconButton from "@/shared/IconButton.svelte";
    import { icons } from "@/shared/icons";
    import type { LabSession } from "@/lab/session.svelte";
    import { demos } from "@/lab/session.svelte";

    let { session }: { session: LabSession } = $props();
</script>

{#each demos as demo (demo.value)}
    <button type="button" aria-pressed={session.demo === demo.value} onclick={() => session.select(demo.value)}>
        {demo.label}
    </button>
{/each}
<IconButton label={session.running ? "Stop" : "Run"} icon={session.running ? icons.stop : icons.play} onclick={() => session.toggle()} />
