<script lang="ts">
  import { onMount } from "svelte";
  import { AlertTriangle, CheckCircle } from "@lucide/svelte";
  import { toast } from "svelte-sonner";
  import { api } from "$lib/api";

  let alerts = $state<any[]>([]);
  let loading = $state(true);
  let resolving = $state<Set<number>>(new Set());

  onMount(async () => {
    try {
      alerts = await api.staffGetAlerts(true);
    } catch (err: any) {
      toast.error(err.message || "Failed to load alerts");
    } finally {
      loading = false;
    }
  });

  async function handleResolve(alertId: number) {
    resolving.add(alertId);
    try {
      await api.staffResolveAlert(alertId);
      alerts = alerts.filter((a) => a.id !== alertId);
      toast.success("Alert resolved");
    } catch (err: any) {
      toast.error(err.message || "Failed to resolve alert");
    } finally {
      resolving.delete(alertId);
    }
  }
</script>

<div class="mb-6">
  <h1 class="font-headline-h2 text-headline-h2 text-ivory-white">Stock Alerts</h1>
  <p class="text-muted-gray text-sm mt-1">Unresolved inventory alerts</p>
</div>

<div class="space-y-4">
  {#if loading}
    <p class="text-muted-gray">Loading...</p>
  {:else if alerts.length === 0}
    <div class="bg-surface-card rounded-2xl border border-deep-border p-8 text-center">
      <AlertTriangle size={48} class="text-green-400 mx-auto mb-3" />
      <p class="text-ivory-white font-medium">No unresolved alerts</p>
      <p class="text-muted-gray text-sm mt-1">All stock levels are healthy</p>
    </div>
  {:else}
    {#each alerts as alert}
      <div class="bg-surface-card rounded-2xl border border-deep-border p-4">
        <div class="flex items-start gap-4">
          <AlertTriangle size={24} class={alert.type === "out_of_stock" ? "text-red-400 shrink-0" : "text-yellow-400 shrink-0"} />
          <div class="flex-1">
            <h4 class="text-ivory-white font-bold">{alert.ingredient_name}</h4>
            <p class="text-muted-gray text-sm mt-1">{alert.message}</p>
            <div class="flex gap-4 mt-2 text-xs text-muted-gray">
              <span>SKU: {alert.ingredient_sku}</span>
              <span>Stock: {Number(alert.stock_qty).toFixed(2)}</span>
              <span>Min: {Number(alert.min_stock).toFixed(2)}</span>
            </div>
          </div>
          <div class="flex flex-col items-end gap-2 shrink-0">
            <span class={`text-xs px-3 py-1 rounded-full font-medium ${alert.type === "out_of_stock" ? "bg-red-500/10 text-red-400" : "bg-yellow-500/10 text-yellow-400"}`}>
              {alert.type === "out_of_stock" ? "OUT OF STOCK" : "LOW STOCK"}
            </span>
            <button
              onclick={() => handleResolve(alert.id)}
              disabled={resolving.has(alert.id)}
              class="flex items-center gap-1 px-3 py-1.5 rounded-lg text-xs font-medium text-green-400 hover:bg-green-500/10 border border-green-500/30 hover:border-green-400/50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors cursor-pointer"
            >
              <CheckCircle size={14} />
              {resolving.has(alert.id) ? "Resolving..." : "Resolve"}
            </button>
          </div>
        </div>
      </div>
    {/each}
  {/if}
</div>
