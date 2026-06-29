<script lang="ts">
  import { onMount } from "svelte";
  import { goto } from "$app/navigation";
  import { page } from "$app/stores";
  import { ArrowLeft } from "@lucide/svelte";
  import { api } from "$lib/api";
  import { auth } from "$lib/stores/auth";
  import { get } from "svelte/store";

  let order = $state<any>(null);
  let loading = $state(true);

  const id = $page.params.id;

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
      order = await api.getMyOrder(Number(id));
    } catch { /* empty */ }
    finally {
      loading = false;
    }
  });

  async function cancelOrder() {
    if (!confirm("Are you sure you want to cancel this order?")) return;
    try {
      order = await api.cancelOrder(Number(id));
    } catch { /* empty */ }
  }
</script>

<a href="/dashboard/orders" class="inline-flex items-center gap-2 text-muted-gray hover:text-flame-orange transition-colors mb-6">
  <ArrowLeft size={16} /> Back to Orders
</a>

{#if loading}
  <div class="flex items-center justify-center min-h-[40vh]">
    <p class="text-muted-gray">Loading order...</p>
  </div>
{:else if order}
  <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
    <!-- Order Items -->
    <div class="lg:col-span-2">
      <div class="bg-surface-card rounded-[1.5rem] border border-deep-border p-6">
        <div class="flex items-center justify-between mb-6">
          <h1 class="font-headline-h2 text-headline-h2 text-ivory-white">{order.order_number}</h1>
          <span class={"text-[10px] font-bold uppercase tracking-widest px-3 py-1 rounded-full border " + statusStyle(order.status)}>
            {order.status}
          </span>
        </div>
        <div class="space-y-4">
          {#each order.items as item}
            <div class="flex justify-between items-center border-b border-deep-border pb-3">
              <div>
                <p class="text-ivory-white font-medium">{item.menu_item_name}</p>
                <p class="text-muted-gray text-sm">x{item.qty} @ ${Number(item.unit_price).toFixed(2)}</p>
              </div>
              <span class="text-ivory-white font-bold">${Number(item.subtotal).toFixed(2)}</span>
            </div>
          {/each}
        </div>
        <div class="mt-6 flex justify-between text-ivory-white font-bold text-lg">
          <span>Total</span>
          <span>${Number(order.total_price).toFixed(2)}</span>
        </div>
      </div>
    </div>

    <!-- Sidebar Info -->
    <div class="space-y-4">
      <div class="bg-surface-card rounded-[1.5rem] border border-deep-border p-6">
        <h3 class="font-headline-h3 text-headline-h3 text-ivory-white mb-4">Payment</h3>
        <div class="space-y-3">
          <div class="flex justify-between text-sm">
            <span class="text-muted-gray">Method</span>
            <span class="text-ivory-white capitalize">{order.payment_method || "-"}</span>
          </div>
          <div class="flex justify-between text-sm">
            <span class="text-muted-gray">Status</span>
            <span class="text-ivory-white capitalize">{order.payment_status}</span>
          </div>
          <div class="flex justify-between text-sm">
            <span class="text-muted-gray">Date</span>
            <span class="text-ivory-white">{new Date(order.created_at).toLocaleDateString()}</span>
          </div>
        </div>
      </div>

      {#if order.status === "pending"}
        <button onclick={cancelOrder} class="w-full border-2 border-red-500 text-red-400 py-3 rounded-xl font-bold hover:bg-red-500/10 transition-all cursor-pointer">
          Cancel Order
        </button>
      {/if}
    </div>
  </div>
{/if}