<script lang="ts" generics="Value extends string">
    import Option from "@/shared/choice/Option.svelte";
    import { type ChoiceOption, RadioChoice } from "@/shared/choice/radio.svelte";

    let { label, options, value = $bindable() }: { label: string; options: readonly ChoiceOption<Value>[]; value: Value } = $props();

    const id = $props.id();
    const choice = new RadioChoice({ id, options: () => options, value: () => value, choose: (picked: Value) => (value = picked) });
</script>

<div class="choice" {...choice.api.getRootProps()} aria-label={label} {@attach choice.root.attach}>
    {#each options as option (option.value)}
        <Option {option} api={choice.api} />
    {/each}
</div>

<style>
    .choice {
        display: flex;
        flex-wrap: wrap;
        gap: 0.4rem;
    }
</style>
