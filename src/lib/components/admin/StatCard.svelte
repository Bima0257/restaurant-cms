<script lang="ts">
  let {
    title,
    value,
    icon,
    trend,
    trendUp = true,
    class: className = "",
  }: {
    title: string;
    value: string;
    icon: any;
    trend?: string;
    trendUp?: boolean;
    class?: string;
  } = $props();
</script>

<div class="bg-surface-card rounded-2xl p-6 border border-deep-border {className}">
  <div class="flex items-start justify-between mb-4">
    <div>
      <p class="text-muted-gray text-sm">{title}</p>
      <p class="font-headline-h2 text-headline-h2 text-ivory-white mt-1">{value}</p>
    </div>
    <div class="w-12 h-12 rounded-xl bg-flame-orange/10 flex items-center justify-center text-flame-orange">
      <icon size={22}></icon>
    </div>
  </div>
  {#if trend}
    <div class="flex items-center gap-2 text-xs">
      <span class={trendUp ? "text-green-400" : "text-red-400"}>{trend}</span>
      <span class="text-muted-gray">vs last month</span>
    </div>
  {/if}
</div>
