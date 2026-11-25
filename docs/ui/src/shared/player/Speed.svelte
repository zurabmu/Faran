<script lang="ts">
    import { SpeedInput } from "@/shared/player/speed-input.svelte";

    let { speed, disabled, onchange }: { speed: number; disabled: boolean; onchange: (speed: number) => void } = $props();

    const id = $props.id();
    const input = new SpeedInput({ id, speed: () => speed, disabled: () => disabled, onchange: (value: number) => onchange(value) });
</script>

<div class="speed" {...input.api.getRootProps()} {@attach input.root.attach}>
    <label class="label" {...input.api.getLabelProps()}>Speed</label>
    <div class="value" {...input.api.getScrubberProps()}>
        <input class="field" {...input.api.getInputProps()} onmousedown={(event) => input.keepTyping(event)} />
        <span class="unit" aria-hidden="true">×</span>
    </div>
</div>

<style>
    .speed {
        display: flex;
        flex-direction: column;
        gap: 0.1rem;
        padding: 0.22rem 0.6rem 0.26rem;
        border: 1px solid var(--faran-rule-strong, #3e3650);
        border-radius: 2px;
    }

    .speed:is(:hover, :focus-within):not([data-disabled]) {
        border-color: var(--faran-end, #7f83f0);
    }

    .speed[data-scrubbing] {
        background-color: var(--faran-end-wash, rgba(127, 131, 240, 0.14));
    }

    .speed[data-disabled] {
        opacity: 0.5;
    }

    .label {
        color: var(--faran-text-faint, #a59cb5);
        font-size: 0.52rem;
        font-weight: 600;
        letter-spacing: 0.08em;
        line-height: 1;
        text-transform: uppercase;
        cursor: inherit;
    }

    .value {
        display: flex;
        align-items: baseline;
        color: var(--faran-text, #f1ecf4);
        font-family: var(--faran-font-code, ui-monospace, monospace);
        font-size: 0.7rem;
        font-variant-numeric: tabular-nums;
        line-height: 1.1;
    }

    .field {
        width: 4ch;
        margin: 0;
        padding: 0;
        border: none;
        background: none;
        color: inherit;
        font: inherit;
        cursor: inherit;
        outline: none;
    }

    .field:focus {
        cursor: text;
    }

    .unit {
        color: var(--faran-text-faint, #a59cb5);
    }
</style>
