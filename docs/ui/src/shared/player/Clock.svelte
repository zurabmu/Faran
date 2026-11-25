<script lang="ts">
    let { step, last, seconds, endSeconds }: { step: number; last: number; seconds: number; endSeconds: number } = $props();

    const lastLabel = $derived(String(last));
    const endLabel = $derived(endSeconds.toFixed(2));
</script>

<div class="clock" role="group" aria-label="Replay position">
    <div class="reading">
        <span class="label">Step</span>
        <span class="value">
            <span class="current" style:min-width="{lastLabel.length}ch">{step}</span>
            <span class="total">/ {lastLabel}</span>
        </span>
    </div>
    <div class="reading">
        <span class="label">Time</span>
        <span class="value">
            <span class="current" style:min-width="{endLabel.length}ch">{seconds.toFixed(2)}</span>
            <span class="total">/ {endLabel} s</span>
        </span>
    </div>
</div>

<style>
    .clock {
        display: flex;
        border: 1px solid var(--faran-rule, #2b2636);
        border-radius: 2px;
        background-color: var(--faran-bg, #0f0d17);
    }

    .reading {
        display: flex;
        flex-direction: column;
        gap: 0.1rem;
        padding: 0.22rem 0.6rem 0.26rem;
    }

    .reading + .reading {
        border-left: 1px solid var(--faran-rule, #2b2636);
    }

    .label {
        color: var(--faran-text-faint, #a59cb5);
        font-size: 0.52rem;
        font-weight: 600;
        letter-spacing: 0.08em;
        line-height: 1;
        text-transform: uppercase;
    }

    .value {
        display: flex;
        align-items: baseline;
        gap: 0.3em;
        font-family: var(--faran-font-code, ui-monospace, monospace);
        font-size: 0.7rem;
        font-variant-numeric: tabular-nums;
        line-height: 1.1;
        white-space: nowrap;
    }

    .current {
        color: var(--faran-text, #f1ecf4);
        text-align: right;
    }

    .total {
        color: var(--faran-text-faint, #a59cb5);
    }
</style>
