<script lang="ts">
  import { onMount } from "svelte";
  import { goto } from "$app/navigation";
  import { page } from "$app/stores";
  import { ArrowLeft } from "@lucide/svelte";
  import { toast } from "svelte-sonner";
  import { confirmAction } from "$lib/utils/confirm";
  import { api } from "$lib/api";
  import { auth } from "$lib/stores/auth";
  import { get } from "svelte/store";

  let order = $state<any>(null);
  let loading = $state(true);

  const id = $page.params.id;

   onMount(async () => {
    if (!get(auth)) {
      goto("/auth/login");
      return;
    }
    try {
      order = await api.getMyOrder(Number(id));
    } catch (err: any) {
      toast.error(err.message || "Failed to load order");
    } finally {
      loading = false;
    }
  });

  async function cancelOrder() {
    const confirmed = await confirmAction({
      title: "Cancel Order",
      message: "Are you sure you want to cancel this order?",
      confirmLabel: "Cancel Order",
      variant: "danger",
    });
    if (!confirmed) return;
    try {
      order = await api.cancelOrder(Number(id));
      toast.success("Order cancelled successfully");
    } catch (err: any) {
      toast.error(err.message);
    }
  }

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
  <a href="/account/orders" class="inline-flex items-center gap-2 text-muted-gray hover:text-flame-orange transition-colors mb-6">
    <ArrowLeft size={16} /> Back to Orders
  </a>

  {#if loading}
    <p class="text-muted-gray">Loading...</p>
  {:else if order}
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <div class="lg:col-span-2">
        <div class="bg-surface-card rounded-2xl border border-deep-border p-6">
          <h1 class="font-headline-h2 text-headline-h2 text-ivory-white mb-2">{order.order_number}</h1>
          <span class={`text-sm font-medium ${statusColor(order.status)}`}>{order.status}</span>
          <div class="mt-6 space-y-4">
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
      <div class="space-y-4">
        <div class="bg-surface-card rounded-2xl border border-deep-border p-6">
          <h3 class="font-headline-h3 text-headline-h3 text-ivory-white mb-3">Payment</h3>
          <p class="text-muted-gray text-sm">
            Method: <span class="text-ivory-white capitalize">{order.payment_method || "-"}</span>
          </p>
          <p class="text-muted-gray text-sm">
            Status: <span class="text-ivory-white capitalize">{order.payment_status}</span>
          </p>
        </div>
        {#if order.status === "pending"}
          <button onclick={cancelOrder} class="w-full border-2 border-red-500 text-red-400 py-3 rounded-full font-bold hover:bg-red-500/10 transition-all cursor-pointer">
            Cancel Order
          </button>
        {/if}
      </div>
    </div>
  {/if}
</div>
