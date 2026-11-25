<script lang="ts">
    import type { Snippet } from "svelte";

    let { children }: { children: Snippet } = $props();
</script>

<span class="actions">{@render children()}</span>

<style>
    .actions {
        display: flex;
        flex-wrap: wrap;
        gap: 0.4rem;
    }

    .actions :global(:is(a, button)) {
        display: inline-flex;
        align-items: center;
        min-height: 1.6rem;
        padding: 0 0.6rem;
        border: 1px solid var(--faran-rule-strong, #3e3650);
        border-radius: 2px;
        background: none;
        color: var(--faran-text, #f1ecf4);
        font-family: inherit;
        font-size: 0.66rem;
        font-weight: 600;
        text-decoration: none;
        cursor: pointer;
    }

    .actions :global(button:has(> .icon:only-child)) {
        justify-content: center;
        width: 1.6rem;
        padding: 0;
    }

    .actions :global(:is(a, button:enabled):is(:hover, :focus-visible, [aria-pressed="true"])) {
        border-color: var(--faran-end, #7f83f0);
        color: var(--faran-end-text, #a3a6ff);
    }

    .actions :global(button:disabled) {
        cursor: default;
        opacity: 0.5;
    }

    .actions :global(button[aria-pressed="true"]) {
        background-color: var(--faran-end-wash, rgba(127, 131, 240, 0.14));
    }

    @media (pointer: coarse) {
        .actions :global(:is(a, button)) {
            min-height: 2.75rem;
            padding: 0 0.9rem;
        }

        .actions :global(button:has(> .icon:only-child)) {
            width: 2.75rem;
            padding: 0;
        }
    }
</style>
