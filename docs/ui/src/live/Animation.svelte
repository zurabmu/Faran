<script lang="ts">
    import type { Animation } from "@engine";
    import type { AnimationPlayer } from "@/shared/player";
    import { mountPlayed } from "@/live/animation";

    let { animation, player }: { animation: Animation; player: AnimationPlayer } = $props();
</script>

<div class="animation" {@attach (element) => mountPlayed({ element, animation, player })}></div>
