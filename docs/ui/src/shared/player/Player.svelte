<script lang="ts">
    import type { Snippet } from "svelte";
    import type { Attachment } from "svelte/attachments";
    import Actions from "@/shared/Actions.svelte";
    import { Bar, Frame, Title, View } from "@/shared/frame";
    import IconButton from "@/shared/IconButton.svelte";
    import { icons } from "@/shared/icons";
    import { hasSteps, type PlayerControls } from "@/shared/player/controls";
    import { Expansion } from "@/shared/player/expansion.svelte";
    import { SourcePanel } from "@/shared/player/source.svelte";
    import SourceRegion from "@/shared/player/SourceRegion.svelte";
    import Transport from "@/shared/player/Transport.svelte";

    let {
        title,
        player,
        actions,
        children,
        source,
        hasPlayback,
        attachSourceButton,
    }: {
        title: string;
        player: PlayerControls;
        actions: Snippet<[boolean]>;
        children: Snippet;
        source: Snippet;
        hasPlayback: boolean;
        attachSourceButton: Attachment<HTMLElement>;
    } = $props();

    const expansion = new Expansion();
    const panel = new SourcePanel();
    const isPlayable = $derived(hasPlayback && hasSteps(player));
</script>

<svelte:window onkeydown={(event) => expansion.shrinkOnEscape(event)} />

<div class="place" style:height={expansion.reservedHeight}>
    <div
        class="player"
        class:expanded={expansion.expanded}
        popover={expansion.expanded ? "manual" : undefined}
        style:view-transition-name={expansion.transitioning ? "faran-expansion" : undefined}
        {@attach expansion.attach}
    >
        <Frame {title}>
            <Bar edge="top">
                <Title text={title} />
                <span class="end">
                    <Actions>{@render actions(panel.open)}</Actions>
                    <Actions>
                        <IconButton
                            label={expansion.expanded ? "Exit full screen" : "Full screen"}
                            icon={expansion.expanded ? icons.collapse : icons.expand}
                            onclick={() => expansion.toggle()}
                        />
                    </Actions>
                </span>
            </Bar>
            <View>
                <div class="stage">{@render children()}</div>
            </View>
            <Bar edge="bottom">
                <Actions>
                    <IconButton label="Show code" icon={icons.code} aria-pressed={panel.open} onclick={() => panel.toggle()} {@attach attachSourceButton} />
                </Actions>
                {#if isPlayable}
                    <Transport {player} />
                {/if}
            </Bar>
            <SourceRegion {panel}>{@render source()}</SourceRegion>
        </Frame>
    </div>
</div>

<style>
    .player:popover-open {
        position: fixed;
        inset: 0;
        width: auto;
        max-width: none;
        height: auto;
        max-height: none;
        margin: 0;
        padding: 0;
        overflow: hidden;
        border: none;
        background: none;
        color: inherit;
    }

    .player.expanded {
        height: 100%;
    }

    .end {
        display: flex;
        flex-wrap: wrap;
        gap: 0.4rem;
        margin-left: auto;
    }

    .expanded .stage,
    .expanded .stage > :global(*) {
        height: 100%;
        min-height: 0;
    }
</style>
