<svelte:options customElement={{ tag: "faran-variants", props: { label: { type: "String" } } }} />

<script lang="ts">
    import { Choice } from "@/shared/choice";
    import { showLinkedSlots } from "@/shared/dom/linked";
    import { VariantChoice } from "@/variants/choice.svelte";
    import { readVariants } from "@/variants/variants";

    let { label }: { label: string } = $props();

    const element = $host();
    const variants = readVariants(element);
    const choice = $derived(new VariantChoice(label, variants));

    $effect(() => showLinkedSlots(element, (slot) => choice.chooseSlot(slot)));
</script>

<div class="variants">
    <Choice {label} options={choice.options} bind:value={() => choice.shown.name, (name) => choice.choose(name)} />
    <svelte:element this={"slot"} name={choice.shown.slot} />
</div>

<style>
    .variants {
        display: flex;
        flex-direction: column;
        gap: 0.7rem;
        padding: 0.9rem;
        border: 1px solid var(--faran-rule, #2b2636);
        border-radius: 2px;
        background: var(--faran-surface, #17141f);
    }
</style>
