<script lang="ts">
  import { onMount } from "svelte";
  import { goto } from "$app/navigation";
  import { ShoppingBag } from "@lucide/svelte";
  import { api } from "$lib/api";
  import { auth } from "$lib/stores/auth";
  import { get } from "svelte/store";

  let orders = $state<any[]>([]);
  let loading = $state(true);

  function statusStyle(status: string) {
    const styles: Record<string, string> = {
      pending: "bg-yellow-500/10 text-yellow-400 border-yellow-500/30",
      confirmed: "bg-blue-500/10 text-blue-400 border-blue-500/30",
      preparing: "bg-flame-orange/10 text-flame-orange border-flame-orange/30",
      ready: "bg-green-500/10 text-green-400 border-green-500/30",
      delivered: "bg-green-500/10 text-green-400 border-green-500/30",
      completed: "bg-green-500/10 text-green-400 border-green-500/30",
      cancelled: "bg-red-500/10 text-red-400 border-red-500/30",
    };
    return styles[status] || "bg-surface-charcoal text-muted-gray border-deep-border";
  }

  onMount(async () => {
    if (!get(auth)) {
      goto("/auth/login");
      return;
    }
    try {
      orders = await api.getMyOrders();
    } catch { /* empty state handles this */ }
    finally {
      loading = false;
    }
  });
</script>

<div class="mb-8">
  <h1 class="font-headline-h1 text-headline-h1 text-ivory-white mb-1">My Orders</h1>
  <p class="text-muted-gray text-body-lg">Track and review your culinary journeys.</p>
</div>

{#if loading}
  <div class="flex items-center justify-center min-h-[40vh]">
    <p class="text-muted-gray">Loading orders...</p>
  </div>
{:else if orders.length === 0}
  <div class="flex flex-col items-center justify-center min-h-[40vh] gap-4">
    <div class="w-16 h-16 bg-surface-charcoal rounded-full flex items-center justify-center">
      <ShoppingBag size={32} class="text-muted-gray" />
    </div>
    <p class="text-muted-gray text-lg">No orders yet</p>
    <a href="/dashboard/menu" class="bg-flame-orange hover:bg-flame-hover text-ivory-white px-8 py-3 rounded-full font-bold text-sm transition-all">
      Browse Menu
    </a>
  </div>
{:else}
  <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
    {#each orders as order}
      <a href="/dashboard/orders/{order.id}" class="block bg-surface-card rounded-[1.5rem] p-5 border border-deep-border hover:translate-y-[-4px] hover:border-flame-orange/50 transition-all duration-300 group">
        <div class="flex items-start justify-between mb-4">
          <span class="text-ivory-white font-bold text-lg">{order.order_number}</span>
          <span class={"text-[10px] font-bold uppercase tracking-widest px-3 py-1 rounded-full border " + statusStyle(order.status)}>
            {order.status}
          </span>
        </div>
        <div class="flex items-center gap-2 text-sm text-muted-gray mb-4">
          <span>{new Date(order.created_at).toLocaleDateString()}</span>
          <span class="w-1 h-1 bg-muted-gray rounded-full"></span>
          <span>{order.items?.length || 0} items</span>
        </div>
        <div class="flex items-center justify-between pt-4 border-t border-deep-border">
          <span class="text-xs text-muted-gray">Total</span>
          <span class="font-label-price text-label-price text-ivory-white">${Number(order.total_price).toFixed(2)}</span>
        </div>
      </a>
    {/each}
  </div>
{/if}