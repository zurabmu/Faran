<svelte:options customElement={{ tag: "faran-docs-map" }} />

<script lang="ts">
    import Loading from "@/shared/Loading.svelte";
    import { SceneView } from "@/shared/scene";
    import { destinationsOf } from "@/docsmap/destinations";
    import { MapView } from "@/docsmap/view.svelte";

    const view = new MapView(destinationsOf($host()));
    const { layout, session, homePress } = view;

    $effect(() => () => view.stop());
</script>

<div
    class="map"
    style:aspect-ratio="{layout.width} / {layout.height}"
    {@attach (element) => view.startWhenVisible(element)}
>
    {#if session.ready}
        <div class="scene"><SceneView renderings={view.renderings} bounds={view.bounds} padding={0} /></div>
    {/if}
    <button
        type="button"
        class="destination home upper"
        class:aimed={session.aimedAt === view.home}
        class:pressed={homePress.pressed}
        style:left={view.homePosition.left}
        style:top={view.homePosition.top}
        aria-current="page"
        onpointerenter={() => session.aim(view.home)}
        onfocus={() => session.aim(view.home)}
        onclick={(event) => view.pressHome(event)}
        onanimationend={() => homePress.end()}
    >
        <span class="marker"></span>
        <span class="title">Home</span>
        <span class="description">You are here</span>
    </button>
    {#each view.markers as { destination, index, position, room, upper, endAligned } (destination.href)}
        <a
            class="destination"
            class:aimed={session.aimedAt === index}
            class:upper
            class:end={endAligned}
            href={destination.href}
            style:left={position.left}
            style:top={position.top}
            style:--room={room}
            onpointerenter={() => session.aim(index)}
            onfocus={() => session.aim(index)}
        >
            <span class="marker"></span>
            <span class="title">{destination.title}</span>
            <span class="description">{destination.description}</span>
        </a>
    {/each}
</div>
<p class="status" aria-live="polite">
    {#if session.status !== ""}
        <Loading label={session.status} active={!session.failed} />
    {:else if session.stepMilliseconds > 0}
        Faran planned the last step in {Math.round(session.stepMilliseconds)} ms, in your browser.
    {/if}
</p>

<style>
    :host {
        display: block;
        margin: 1.5rem 0 0.4rem;
    }

    .map {
        position: relative;
        width: 100%;
        font-family: var(--faran-font-text, system-ui, sans-serif);
    }

    .scene {
        position: absolute;
        inset: 0;
    }

    .destination {
        position: absolute;
        display: grid;
        grid-template-columns: auto;
        width: min(13rem, calc(var(--room, 100%) + 0.35rem));
        padding: 0;
        border: none;
        background: none;
        color: var(--faran-text-muted, #b8afc6);
        cursor: pointer;
        font: inherit;
        text-align: left;
        text-decoration: none;
        transform: translate(-0.35rem, -0.35rem);
    }

    .destination:not(.upper) {
        transform: translate(-0.35rem, calc(-100% + 0.35rem));
    }

    .destination.end {
        justify-items: end;
        text-align: right;
        transform: translate(calc(-100% + 0.35rem), -0.35rem);
    }

    .destination.end:not(.upper) {
        transform: translate(calc(-100% + 0.35rem), calc(-100% + 0.35rem));
    }

    .home {
        width: 7rem;
    }

    .marker {
        width: 0.7rem;
        height: 0.7rem;
        border: 1px solid var(--faran-end-text, #a3a6ff);
        border-radius: 50%;
        background-color: var(--faran-bg, #0f0d17);
        transition:
            background-color 0.2s,
            border-color 0.2s;
    }

    .home .marker {
        border-color: var(--faran-start-text, #ffa487);
    }

    .destination:not(.upper) .marker {
        order: 3;
        margin-top: 0.3rem;
    }

    .title {
        margin-top: 0.3rem;
        color: var(--faran-text, #f1ecf4);
        font-size: 0.82rem;
        font-weight: 600;
    }

    .description {
        font-size: 0.68rem;
        line-height: 1.45;
    }

    .destination:is(:hover, :focus-visible, .aimed) .marker {
        border-color: var(--faran-start-text, #ffa487);
        background-color: var(--faran-start-text, #ffa487);
    }

    .destination:is(:hover, :focus-visible) .title {
        text-decoration: underline;
        text-decoration-color: var(--faran-end-text, #a3a6ff);
        text-decoration-thickness: 2px;
        text-underline-offset: 0.22em;
    }

    .destination:focus-visible {
        outline: none;
    }

    .home.pressed .marker {
        animation: press 0.45s cubic-bezier(0.22, 0.61, 0.36, 1);
    }

    @keyframes press {
        30% {
            transform: scale(0.6);
        }

        100% {
            transform: scale(1);
        }
    }

    .status {
        min-height: 1.2em;
        margin: 0;
        color: var(--faran-text-faint, #a59cb5);
        font-family: var(--faran-font-text, system-ui, sans-serif);
        font-size: 0.7rem;
    }

    @media (prefers-reduced-motion: reduce) {
        .home.pressed .marker {
            animation: none;
        }
    }

    @media screen and (max-width: 44.984375em) {
        .map {
            aspect-ratio: auto !important;
        }

        .scene,
        .home {
            display: none;
        }

        .destination,
        .destination:not(.upper),
        .destination.end,
        .destination.end:not(.upper) {
            position: static;
            width: auto;
            margin-bottom: 0.9rem;
            justify-items: start;
            text-align: left;
            transform: none;
        }

        .destination:not(.upper) .marker {
            order: 0;
        }
    }
</style>
