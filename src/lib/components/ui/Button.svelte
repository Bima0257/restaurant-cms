<script lang="ts">
  let {
    variant = "primary",
    size = "md",
    href,
    class: className = "",
    children,
    ...rest
  }: {
    variant?: "primary" | "outline" | "ghost";
    size?: "sm" | "md" | "lg";
    href?: string;
    class?: string;
    children?: import("svelte").Snippet;
  } = $props();

  const base = "inline-flex items-center justify-center font-bold transition-all rounded-full cursor-pointer";

  const variants: Record<string, string> = {
    primary: "bg-flame-orange hover:bg-flame-hover text-ivory-white orange-glow hover:scale-105",
    outline: "border-2 border-flame-orange text-flame-orange hover:bg-flame-orange hover:text-white uppercase tracking-widest text-xs",
    ghost: "text-ivory-white font-medium hover:text-flame-orange transition-colors duration-300",
  };

  const sizes: Record<string, string> = {
    sm: "px-4 py-2 text-sm",
    md: "px-8 py-4",
    lg: "px-10 py-4",
  };
</script>

{#if href}
  <a href={href} class="{base} {variants[variant]} {sizes[size]} {className}" {...rest}>
    {@render children?.()}
  </a>
{:else}
  <button class="{base} {variants[variant]} {sizes[size]} {className}" {...rest}>
    {@render children?.()}
  </button>
{/if}
