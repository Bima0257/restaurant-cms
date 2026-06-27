<script lang="ts">
  import { Star } from "@lucide/svelte";

  let {
    value = 0,
    max = 5,
    size = 14,
    color = "text-flame-orange",
    class: className = "",
  }: {
    value?: number;
    max?: number;
    size?: number;
    color?: string;
    class?: string;
  } = $props();
</script>

<div class="flex gap-0.5 {className}">
  {#each Array(max) as _, i}
    <Star
      size={size}
      class={i < value ? color : "text-muted-gray"}
      fill={i < value ? "currentColor" : "none"}
    />
  {/each}
</div>
