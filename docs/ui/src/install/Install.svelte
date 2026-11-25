<svelte:options customElement={{ tag: "faran-install" }} />

<script lang="ts">
    import { Choice } from "@/shared/choice";
    import CopyButton from "@/shared/CopyButton.svelte";
    import { type Backend, backends, installCommand } from "@/install/command";

    let backend = $state<Backend>("numpy");
    let visualizer = $state(true);
    const command = $derived(installCommand({ backend, visualizer }));
</script>

<div class="install">
    <Choice label="Backend" options={backends} bind:value={backend} />
    <label class="toggle">
        <input type="checkbox" bind:checked={visualizer} />
        <span>Add the visualizer, a separate package for interactive HTML replays</span>
    </label>
    <div class="command">
        <code><span class="prompt">$</span> {command}</code>
        <CopyButton text={command} />
    </div>
    <p class="note">Faran needs Python 3.13 or newer.</p>
</div>

<style>
    .install {
        display: flex;
        flex-direction: column;
        gap: 0.7rem;
        margin: 1em 0;
        padding: 0.9rem;
        border: 1px solid var(--faran-rule, #2b2636);
        border-radius: 2px;
        background: var(--faran-surface, #17141f);
        color: var(--faran-text, #f1ecf4);
        font-family: var(--faran-font-text, system-ui, sans-serif);
    }

    .toggle {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        color: var(--faran-text-muted, #b8afc6);
        font-size: 0.7rem;
        cursor: pointer;
    }

    .toggle input {
        display: grid;
        flex: none;
        place-content: center;
        width: 0.85rem;
        height: 0.85rem;
        margin: 0;
        border: 1px solid var(--faran-rule-strong, #3e3650);
        border-radius: 2px;
        background: none;
        cursor: pointer;
        appearance: none;
    }

    .toggle input:checked {
        border-color: var(--faran-end-text, #a3a6ff);
        background-color: var(--faran-end-text, #a3a6ff);
    }

    .toggle input:checked::after {
        content: "";
        width: 0.22rem;
        height: 0.42rem;
        margin-top: -0.08rem;
        border: solid var(--faran-bg, #0f0d17);
        border-width: 0 1.5px 1.5px 0;
        transform: rotate(45deg);
    }

    .toggle input:focus-visible {
        outline: 2px solid var(--faran-end-text, #a3a6ff);
        outline-offset: 2px;
    }

    .command {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 0.8rem;
        padding: 0.55rem 0.7rem;
        border-left: 2px solid var(--faran-start, #f08a6a);
        background: var(--faran-code-bg, #14111c);
    }

    code {
        min-width: 0;
        overflow-x: auto;
        color: var(--faran-code-name, #ece5ef);
        font: 0.75rem/1.5 var(--faran-font-code, ui-monospace, monospace);
        white-space: nowrap;
    }

    .prompt {
        color: var(--faran-text-faint, #a59cb5);
        user-select: none;
    }

    .note {
        margin: 0;
        color: var(--faran-text-muted, #b8afc6);
        font-size: 0.66rem;
    }
</style>
