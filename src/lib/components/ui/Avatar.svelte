<script lang="ts">
  let {
    src,
    alt = "avatar",
    size = "md",
    border = false,
    class: className = "",
  }: {
    src: string;
    alt?: string;
    size?: "sm" | "md" | "lg";
    border?: boolean;
    class?: string;
  } = $props();

  const sizes: Record<string, string> = {
    sm: "w-10 h-10",
    md: "w-12 h-12",
    lg: "w-14 h-14",
  };
</script>

<img
  src={src}
  alt={alt}
  class="rounded-full object-cover {sizes[size]} {border ? 'border-2 border-flame-orange' : ''} {className}"
/>
