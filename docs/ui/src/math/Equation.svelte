<svelte:options customElement={{ tag: "faran-equation", props: { number: { type: "String" } } }} />

<script lang="ts">
    import { siteUrl } from "@/shared/site";
    import Legend from "@/math/Legend.svelte";
    import { EquationLegend } from "@/math/equation-legend.svelte";
    import { typesetMath } from "@/math/typeset";

    let { number }: { number: string } = $props();

    const element = $host();
    typesetMath(element);
    const legend = new EquationLegend(element);
    const katexStyles = siteUrl("assets/katex/katex.min.css").href;
</script>

<svelte:document onpointerdown={(event) => legend.clearOutside(event)} />

<link rel="stylesheet" href={katexStyles} />
<div class="body">
    <slot name="formula" />
    <span class="number">{number}</span>
</div>
<slot />
{#if legend.symbols.length > 0}
    <Legend {legend} />
{/if}

<style>
    :host {
        display: block;
        margin: 1.6em 0;
        border: 1px solid var(--faran-rule, #2b2636);
        border-radius: 2px;
        background-color: var(--faran-surface, #17141f);
    }

    .body {
        display: grid;
        grid-template-columns: minmax(0, 1fr) auto;
        align-items: center;
        gap: 1rem;
        padding: 0.8rem 1rem 0.8rem 1.2rem;
    }

    .number {
        color: var(--faran-text-muted, #c9c0d4);
        font-variant-numeric: tabular-nums;
    }
</style>
