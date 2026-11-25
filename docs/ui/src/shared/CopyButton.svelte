<script lang="ts">
    import { CopyFeedback } from "@/shared/copy-feedback.svelte";
    import Icon from "@/shared/Icon.svelte";
    import { icons } from "@/shared/icons";

    let { text }: { text: string } = $props();

    const feedback = new CopyFeedback();
</script>

<button
    type="button"
    class="copy"
    data-state={feedback.state}
    aria-label={feedback.state === "copied" ? "Copied" : "Copy"}
    title={feedback.state === "copied" ? "Copied" : "Copy"}
    onclick={() => feedback.copy(text)}
>
    {#if feedback.state === "refused"}
        Select and copy
    {:else}
        <Icon path={feedback.state === "copied" ? icons.check : icons.copy} />
    {/if}
</button>

<style>
    .copy {
        display: inline-flex;
        flex: none;
        align-items: center;
        padding: 0.35rem 0.6rem;
        border: 1px solid var(--faran-rule-strong, #3e3650);
        border-radius: 2px;
        background: var(--faran-raised, #1f1b2a);
        color: var(--faran-text, #f1ecf4);
        font: 600 0.65rem/1 var(--faran-font-text, system-ui, sans-serif);
        cursor: pointer;
    }

    .copy:hover {
        border-color: var(--faran-end, #7f83f0);
    }

    .copy:focus-visible {
        outline: 2px solid var(--faran-end-text, #a3a6ff);
        outline-offset: 2px;
    }

    .copy[data-state="copied"] {
        border-color: var(--faran-end, #7f83f0);
        color: var(--faran-end-text, #a3a6ff);
    }
</style>
