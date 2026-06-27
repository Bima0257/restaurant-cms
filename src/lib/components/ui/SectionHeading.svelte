<script lang="ts">
  let {
    prefix,
    highlight,
    class: className = "",
  }: {
    prefix: string;
    highlight: string;
    class?: string;
  } = $props();
</script>

<h2 class="signature-bracket {className}">
  {prefix} <span class="text-flame-orange">{highlight}</span>
</h2>
