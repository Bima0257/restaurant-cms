<script lang="ts">
  import { onMount } from "svelte";
  import { goto } from "$app/navigation";
  import { toast } from "svelte-sonner";
  import { api } from "$lib/api";
  import { auth } from "$lib/stores/auth";
  import { get } from "svelte/store";

  let orders = $state<any[]>([]);
  let loading = $state(true);

   onMount(async () => {
    if (!get(auth)) {
      goto("/auth/login");
      return;
    }
    try {
      orders = await api.getMyOrders();
    } catch (err: any) {
      toast.error(err.message || "Failed to load orders");
    } finally {
      loading = false;
    }
  });

  function statusColor(status: string) {
    const colors: Record<string, string> = {
      pending: "text-yellow-400",
      confirmed: "text-blue-400",
      preparing: "text-flame-orange",
      ready: "text-green-400",
      delivered: "text-green-400",
      completed: "text-green-400",
      cancelled: "text-red-400",
    };
    return colors[status] || "text-muted-gray";
  }
</script>

<div class="pt-32 pb-20 px-gutter max-w-grid-max-width mx-auto">
  <h1 class="font-headline-h1 text-headline-h1 mb-8">My Orders</h1>

  {#if loading}
    <p class="text-muted-gray">Loading...</p>
  {:else if orders.length === 0}
    <div class="text-center py-20">
      <p class="text-muted-gray text-lg mb-4">No orders yet</p>
      <a href="/menu" class="bg-flame-orange hover:bg-flame-hover text-ivory-white px-8 py-3 rounded-full font-bold inline-block">Browse Menu</a>
    </div>
  {:else}
    <div class="space-y-4">
      {#each orders as order}
        <a href="/account/orders/{order.id}" class="block bg-surface-card rounded-2xl border border-deep-border p-6 hover:border-flame-orange/50 transition-colors">
          <div class="flex justify-between items-center mb-2">
            <span class="text-ivory-white font-bold">{order.order_number}</span>
            <span class={`text-sm font-medium ${statusColor(order.status)}`}>{order.status}</span>
          </div>
          <div class="flex justify-between text-sm">
            <span class="text-muted-gray">{new Date(order.created_at).toLocaleDateString()}</span>
            <span class="text-flame-orange font-bold">${Number(order.total_price).toFixed(2)}</span>
          </div>
        </a>
      {/each}
    </div>
  {/if}
</div>
