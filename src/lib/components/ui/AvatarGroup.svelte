<script lang="ts">
  let {
    avatars,
    surplus,
    size = "sm",
    overlap = true,
    class: className = "",
  }: {
    avatars: { src: string; alt?: string }[];
    surplus?: number;
    size?: "sm" | "md" | "lg";
    overlap?: boolean;
    class?: string;
  } = $props();

  const sizes: Record<string, string> = {
    sm: "w-10 h-10",
    md: "w-12 h-12",
    lg: "w-14 h-14",
  };
</script>

<div class="flex {overlap ? '-space-x-3' : 'gap-2'} {className}">
  {#each avatars as avatar}
    <img
      src={avatar.src}
      alt={avatar.alt ?? "avatar"}
      class="{sizes[size]} rounded-full border-2 border-surface object-cover"
    />
  {/each}
  {#if surplus}
    <div class="{sizes[size]} rounded-full bg-flame-orange flex items-center justify-center text-white font-bold text-sm border-2 border-surface">
      {surplus}+
    </div>
  {/if}
</div>
