<script lang="ts">
  let {
    class: className = "",
    hover = true,
    children,
    ...rest
  }: {
    class?: string;
    hover?: boolean;
    children?: import("svelte").Snippet;
  } = $props();
</script>

<div
  class="bg-surface-card rounded-3xl p-6 {hover ? 'hover:-translate-y-2 transition-transform duration-300' : ''} {className}"
  {...rest}
>
  {@render children?.()}
</div>
