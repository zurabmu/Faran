<script lang="ts" generics="Value extends string">
    import type * as radioGroup from "@zag-js/radio-group";
    import type { ChoiceOption } from "@/shared/choice/radio.svelte";

    let { option, api }: { option: ChoiceOption<Value>; api: radioGroup.Api } = $props();
</script>

<label class="option" {...api.getItemProps({ value: option.value })}>
    <span class="label" {...api.getItemTextProps({ value: option.value })}>{option.label}</span>
    {#if option.note !== ""}
        <span class="note">{option.note}</span>
    {/if}
    <input {...api.getItemHiddenInputProps({ value: option.value })} />
</label>

<style>
    .option {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        gap: 0.15rem;
        padding: 0.45rem 0.7rem;
        border: 1px solid var(--faran-rule-strong, #3e3650);
        border-radius: 2px;
        background: transparent;
        color: var(--faran-text, #f1ecf4);
        font-family: var(--faran-font-text, system-ui, sans-serif);
        text-align: left;
        cursor: pointer;
    }

    .option:hover {
        border-color: var(--faran-text-faint, #a59cb5);
    }

    .option[data-focus-visible] {
        outline: 2px solid var(--faran-end-text, #a3a6ff);
        outline-offset: 2px;
    }

    .option[data-state="checked"] {
        border-color: var(--faran-end, #7f83f0);
        background: var(--faran-end-wash, rgba(127, 131, 240, 0.14));
    }

    .label {
        font-size: 0.72rem;
        font-weight: 600;
    }

    .note {
        color: var(--faran-text-muted, #b8afc6);
        font-size: 0.62rem;
    }
</style>
