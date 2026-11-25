<script lang="ts">
    import type { HintTour } from "@/shared/hint/tour.svelte";

    let { tour }: { tour: HintTour } = $props();
</script>

{#if tour.visible}
    <div
        class="hint"
        style:left="{tour.box.left}px"
        style:top="{tour.box.top}px"
        style:width="{tour.box.width}px"
        style:height="{tour.box.height}px"
    >
        <span class="square" aria-hidden="true">
            <span class="dot"></span>
        </span>
        {#key tour.index}
            <p class="popup {tour.box.placement} {tour.box.alignment}" role="status">{tour.text}</p>
        {/key}
    </div>
{/if}

<style>
    .hint {
        position: absolute;
        z-index: 5;
        pointer-events: none;
        transition:
            left 0.5s cubic-bezier(0.22, 0.61, 0.36, 1),
            top 0.5s cubic-bezier(0.22, 0.61, 0.36, 1),
            width 0.5s cubic-bezier(0.22, 0.61, 0.36, 1),
            height 0.5s cubic-bezier(0.22, 0.61, 0.36, 1);
    }

    .square {
        position: absolute;
        inset: -5px;
        border: 1px solid color-mix(in srgb, var(--faran-start-text, #ffa487) 35%, transparent);
        border-radius: 3px;
        animation: appear 0.3s ease-out;
    }

    .dot {
        position: absolute;
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background-color: var(--faran-start-text, #ffa487);
        box-shadow: 0 0 6px var(--faran-start-text, #ffa487);
        translate: -50% -50%;
        animation: orbit 1.6s linear infinite;
    }

    .popup {
        position: absolute;
        width: max-content;
        max-width: 14rem;
        margin: 0;
        padding: 0.35rem 0.6rem;
        border: 1px solid var(--faran-start-text, #ffa487);
        border-radius: 3px;
        background-color: var(--faran-raised, #1f1b2a);
        color: var(--faran-text, #f1ecf4);
        font-family: var(--faran-font-text, system-ui, sans-serif);
        font-size: 0.66rem;
        line-height: 1.4;
        animation: fade 0.3s 0.2s both;
    }

    .popup.start {
        left: -5px;
    }

    .popup.end {
        right: -5px;
    }

    .popup.below {
        top: calc(100% + 0.7rem);
    }

    .popup.above {
        bottom: calc(100% + 0.7rem);
    }

    @keyframes appear {
        from {
            opacity: 0;
        }
    }

    @keyframes orbit {
        0%,
        100% {
            left: 0;
            top: 0;
        }

        25% {
            left: 100%;
            top: 0;
        }

        50% {
            left: 100%;
            top: 100%;
        }

        75% {
            left: 0;
            top: 100%;
        }
    }

    @keyframes fade {
        from {
            opacity: 0;
            translate: 0 0.25rem;
        }
    }

    @media (prefers-reduced-motion: reduce) {
        .hint {
            transition: none;
        }

        .square,
        .dot,
        .popup {
            animation: none;
        }
    }
</style>
