<svelte:options customElement={{ tag: "faran-backend-switch" }} />

<script lang="ts">
    import { RadioChoice } from "@/shared/choice/radio.svelte";
    import { required } from "@/shared/required";
    import { BACKENDS, type Backend, backendChoice } from "@/backends/choice.svelte";
    import { findBackendEntries, removeBackendPrefixes } from "@/backends/contents";

    const contents = required($host(), "<faran-backend-switch>").next<HTMLElement>('[data-md-component="toc"]', "the table of contents list");
    const entries = findBackendEntries(contents);
    removeBackendPrefixes(entries);

    const options = BACKENDS.map((backend) => ({ value: backend, label: backend, note: "" }));
    const id = $props.id();
    const choice = new RadioChoice({ id, options: () => options, value: () => backendChoice.backend, choose: (backend: Backend) => (backendChoice.backend = backend) });

    $effect(() => {
        for (const { backend, item } of entries) item.hidden = backend !== backendChoice.backend;
    });
</script>

{#if entries.length > 0}
    <div class="switch" {...choice.api.getRootProps()} aria-label="Backend" {@attach choice.root.attach}>
        {#each options as { value, label } (value)}
            <label class="option" {...choice.api.getItemProps({ value })}>
                <span {...choice.api.getItemTextProps({ value })}>{label}</span>
                <input {...choice.api.getItemHiddenInputProps({ value })} />
            </label>
        {/each}
    </div>
{/if}

<style>
    .switch {
        display: inline-flex;
        margin: 0.2rem 0.6rem 0.4rem;
        border: 1px solid var(--faran-rule-strong, #3e3650);
        border-radius: 2px;
    }

    .option {
        padding: 0.15rem 0.55rem;
        border: none;
        background: none;
        color: var(--faran-text-muted, #c9c0d4);
        font: 600 0.62rem/1.4 var(--faran-font-text, system-ui, sans-serif);
        cursor: pointer;
    }

    .option + .option {
        border-left: 1px solid var(--faran-rule-strong, #3e3650);
    }

    .option:is(:hover, [data-focus-visible]) {
        color: var(--faran-text, #f1ecf4);
    }

    .option[data-focus-visible] {
        outline: 2px solid var(--faran-end-text, #ffd8c2);
        outline-offset: 2px;
    }

    .option[data-state="checked"] {
        background-color: var(--faran-end-wash, #2a1f33);
        color: var(--faran-end-text, #ffd8c2);
    }
</style>
