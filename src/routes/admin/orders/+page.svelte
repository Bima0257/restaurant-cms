<script lang="ts">
  import { onMount } from "svelte";
  import { X, Loader2, ChevronDown } from "@lucide/svelte";
  import { toast } from "svelte-sonner";
  import { api } from "$lib/api";
  import SectionHeading from "$lib/components/ui/SectionHeading.svelte";

  let orders = $state<any[]>([]);
  let loading = $state(true);
  let statusFilter = $state("");
  let selectedOrder = $state<any>(null);
  let updatingStatus = $state(false);

  const statusOptions = [
    { value: "", label: "All" },
    { value: "pending", label: "Pending" },
    { value: "confirmed", label: "Confirmed" },
    { value: "preparing", label: "Preparing" },
    { value: "ready", label: "Ready" },
    { value: "delivered", label: "Delivered" },
    { value: "completed", label: "Completed" },
    { value: "cancelled", label: "Cancelled" },
  ];

  const statusColors: Record<string, string> = {
    pending: "text-yellow-400",
    confirmed: "text-blue-400",
    preparing: "text-flame-orange",
    ready: "text-purple-400",
    delivered: "text-green-400",
    completed: "text-green-400",
    cancelled: "text-red-400",
  };

  const statusBg: Record<string, string> = {
    pending: "bg-yellow-500/10 border-yellow-500/20",
    confirmed: "bg-blue-500/10 border-blue-500/20",
    preparing: "bg-flame-orange/10 border-flame-orange/20",
    ready: "bg-purple-500/10 border-purple-500/20",
    delivered: "bg-green-500/10 border-green-500/20",
    completed: "bg-green-500/10 border-green-500/20",
    cancelled: "bg-red-500/10 border-red-500/20",
  };

  onMount(() => { load(); });

  async function load() {
    loading = true;
    try {
      orders = await api.adminListOrders(statusFilter || undefined);
    } catch (err: any) {
      toast.error(err.message || "Failed to load orders");
    } finally {
      loading = false;
    }
  }

  async function setFilter(value: string) {
    statusFilter = value;
    await load();
  }

  let stats = $derived({
    total: orders.length,
    pending: orders.filter((o) => o.status === "pending").length,
    preparing: orders.filter((o) => o.status === "preparing").length,
    completed: orders.filter((o) => o.status === "completed" || o.status === "delivered").length,
  });

  function formatPrice(price: number) {
    return `$${Number(price).toFixed(2)}`;
  }

  function formatDate(dateStr: string) {
    const d = new Date(dateStr);
    return d.toLocaleDateString("en-US", { month: "short", day: "numeric", hour: "2-digit", minute: "2-digit" });
  }

  function openDetail(order: any) {
    selectedOrder = order;
  }

  async function updateStatus(orderId: number, newStatus: string) {
    updatingStatus = true;
    try {
      const updated = await api.adminUpdateOrderStatus(orderId, newStatus);
      orders = orders.map((o) => (o.id === orderId ? updated : o));
      selectedOrder = updated;
      toast.success("Order status updated");
    } catch (err: any) {
      toast.error(err.message);
    } finally {
      updatingStatus = false;
    }
  }

  function label(str: string) {
    return str.charAt(0).toUpperCase() + str.slice(1);
  }
</script>

<div class="mb-8">
  <SectionHeading prefix="Orders" highlight="Management" />
</div>

<div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
  <div class="bg-surface-card rounded-2xl p-4 border border-deep-border">
    <p class="text-muted-gray text-sm">Total Orders</p>
    <p class="font-headline-h2 text-headline-h2 text-ivory-white mt-1">{stats.total}</p>
  </div>
  <div class="bg-surface-card rounded-2xl p-4 border border-deep-border">
    <p class="text-muted-gray text-sm">Pending</p>
    <p class="font-headline-h2 text-headline-h2 text-yellow-400 mt-1">{stats.pending}</p>
  </div>
  <div class="bg-surface-card rounded-2xl p-4 border border-deep-border">
    <p class="text-muted-gray text-sm">Preparing</p>
    <p class="font-headline-h2 text-headline-h2 text-flame-orange mt-1">{stats.preparing}</p>
  </div>
  <div class="bg-surface-card rounded-2xl p-4 border border-deep-border">
    <p class="text-muted-gray text-sm">Completed/Delivered</p>
    <p class="font-headline-h2 text-headline-h2 text-green-400 mt-1">{stats.completed}</p>
  </div>
</div>

<div class="flex items-center gap-2 mb-6 flex-wrap">
  {#each statusOptions as opt}
    <button
      onclick={() => setFilter(opt.value)}
      class="px-4 py-2 rounded-lg text-sm font-medium transition-all cursor-pointer {statusFilter === opt.value ? 'bg-flame-orange text-ivory-white' : 'bg-surface-charcoal text-muted-gray hover:text-ivory-white'}"
    >
      {opt.label}
    </button>
  {/each}
</div>

{#if loading}
  <div class="bg-surface-card rounded-2xl border border-deep-border p-12 text-center">
    <Loader2 size={24} class="animate-spin text-muted-gray mx-auto" />
    <p class="text-muted-gray text-sm mt-2">Loading...</p>
  </div>
{:else if orders.length === 0}
  <div class="bg-surface-card rounded-2xl border border-deep-border p-12 text-center">
    <p class="text-muted-gray">No orders found</p>
  </div>
{:else}
  <div class="bg-surface-card rounded-2xl border border-deep-border overflow-hidden">
    <table class="w-full text-sm">
      <thead>
        <tr class="border-b border-deep-border">
          <th class="text-left py-3 px-4 text-muted-gray font-medium text-[10px] uppercase tracking-wider">Order</th>
          <th class="text-left py-3 px-4 text-muted-gray font-medium text-[10px] uppercase tracking-wider hidden md:table-cell">Date</th>
          <th class="text-left py-3 px-4 text-muted-gray font-medium text-[10px] uppercase tracking-wider hidden lg:table-cell">Items</th>
          <th class="text-left py-3 px-4 text-muted-gray font-medium text-[10px] uppercase tracking-wider">Total</th>
          <th class="text-left py-3 px-4 text-muted-gray font-medium text-[10px] uppercase tracking-wider">Status</th>
          <th class="text-left py-3 px-4 text-muted-gray font-medium text-[10px] uppercase tracking-wider hidden md:table-cell">Payment</th>
        </tr>
      </thead>
      <tbody>
        {#each orders as order}
          <tr
            class="border-b border-deep-border/50 hover:bg-surface-charcoal/40 transition-colors cursor-pointer"
            onclick={() => openDetail(order)}
            onkeydown={(e) => { if (e.key === "Enter") openDetail(order); }}
            role="button"
            tabindex="0"
          >
            <td class="py-3 px-4">
              <p class="text-ivory-white font-medium text-sm">{order.order_number}</p>
              <p class="text-muted-gray text-xs md:hidden">{formatDate(order.created_at)}</p>
            </td>
            <td class="py-3 px-4 text-muted-gray text-sm hidden md:table-cell">{formatDate(order.created_at)}</td>
            <td class="py-3 px-4 text-muted-gray text-sm hidden lg:table-cell">{order.items?.length || 0}</td>
            <td class="py-3 px-4 text-ivory-white text-sm font-medium">{formatPrice(order.total_price)}</td>
            <td class="py-3 px-4">
              <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border {statusBg[order.status] || 'bg-gray-500/10 border-gray-500/20'} {statusColors[order.status] || 'text-muted-gray'}">
                {label(order.status)}
              </span>
            </td>
            <td class="py-3 px-4 text-muted-gray text-sm hidden md:table-cell">{label(order.payment_status)}</td>
          </tr>
        {/each}
      </tbody>
    </table>
  </div>
{/if}

<!-- Order Detail Modal -->
{#if selectedOrder}
  <div class="fixed inset-0 bg-black/60 flex items-center justify-center z-[9999] p-4" onclick={() => selectedOrder = null} onkeydown={(e) => { if (e.key === "Escape") selectedOrder = null; }} role="dialog" aria-modal="true" tabindex="-1">
    <div class="bg-surface-card rounded-3xl p-6 w-full max-w-lg max-h-[90vh] overflow-y-auto" onclick={(e: Event) => e.stopPropagation()} onkeydown={() => {}}>
      <div class="flex items-center justify-between mb-6">
        <div>
          <h2 class="text-ivory-white font-bold text-lg">{selectedOrder.order_number}</h2>
          <p class="text-muted-gray text-xs">{formatDate(selectedOrder.created_at)}</p>
        </div>
        <button onclick={() => selectedOrder = null} class="p-1 rounded-lg hover:bg-surface-charcoal text-muted-gray hover:text-ivory-white transition-colors cursor-pointer"><X size={18} /></button>
      </div>

      <div class="flex gap-2 mb-6">
        <span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium border {statusBg[selectedOrder.status] || 'bg-gray-500/10 border-gray-500/20'} {statusColors[selectedOrder.status] || 'text-muted-gray'}">
          {label(selectedOrder.status)}
        </span>
        <span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium border bg-blue-500/10 text-blue-400 border-blue-500/20">
          {label(selectedOrder.payment_status)}
        </span>
      </div>

      <div class="space-y-3 mb-6">
        <h3 class="text-sm font-medium text-ivory-white">Items</h3>
        {#if selectedOrder.items?.length}
          {#each selectedOrder.items as item}
            <div class="flex items-center justify-between bg-surface-charcoal rounded-xl px-4 py-3">
              <div>
                <p class="text-ivory-white text-sm">{item.menu_item_name || `Item #${item.menu_item_id}`}</p>
                <p class="text-muted-gray text-xs">{item.qty} x {formatPrice(item.unit_price)}</p>
              </div>
              <p class="text-ivory-white text-sm font-medium">{formatPrice(item.subtotal)}</p>
            </div>
          {/each}
        {:else}
          <p class="text-muted-gray text-sm">No items</p>
        {/if}
        <div class="flex items-center justify-between pt-2">
          <p class="text-ivory-white font-bold">Total</p>
          <p class="text-flame-orange font-bold">{formatPrice(selectedOrder.total_price)}</p>
        </div>
      </div>

      {#if selectedOrder.notes}
        <div class="mb-6">
          <h3 class="text-sm font-medium text-ivory-white mb-2">Notes</h3>
          <p class="text-muted-gray text-sm bg-surface-charcoal rounded-xl px-4 py-3">{selectedOrder.notes}</p>
        </div>
      {/if}

      <div>
        <label for="order-status" class="block text-sm text-muted-gray mb-2">Update Status</label>
        <div class="flex gap-2 flex-wrap">
          {#each ["pending", "confirmed", "preparing", "ready", "delivered", "completed", "cancelled"] as s}
            <button
              onclick={() => updateStatus(selectedOrder.id, s)}
              disabled={updatingStatus || selectedOrder.status === s}
              class="px-3 py-1.5 rounded-lg text-xs font-medium transition-all cursor-pointer disabled:opacity-40 disabled:cursor-not-allowed {selectedOrder.status === s ? 'bg-flame-orange text-ivory-white' : 'bg-surface-charcoal text-muted-gray hover:text-ivory-white'}"
            >
              {label(s)}
            </button>
          {/each}
        </div>
      </div>
    </div>
  </div>
{/if}
