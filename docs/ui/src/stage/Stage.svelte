<svelte:options customElement={{ tag: "faran-stage" }} />

<script lang="ts">
    const id = $props.id();
</script>

<div class="stage" aria-hidden="true">
    <svg class="field">
        <defs>
            <pattern id="{id}-points" width="40" height="40" patternUnits="userSpaceOnUse">
                <circle cx="20" cy="20" r="1" />
            </pattern>
        </defs>
        <rect width="100%" height="100%" fill="url(#{id}-points)" />
    </svg>
    <span class="label">Lab placeholder</span>
</div>

<style>
    :host {
        position: fixed;
        inset: 0;
        z-index: 0;
        pointer-events: none;
    }

    .stage {
        position: absolute;
        inset: 0;
    }

    .field {
        width: 100%;
        height: 100%;
    }

    circle {
        fill: var(--faran-rule-strong, #3e3650);
    }

    .label {
        position: absolute;
        right: 1.6rem;
        bottom: 1.2rem;
        color: var(--faran-text-faint, #a59cb5);
        font-family: var(--faran-font-text, system-ui, sans-serif);
        font-size: 0.62rem;
        opacity: 0.6;
    }
</style>
