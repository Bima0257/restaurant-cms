<script lang="ts">
  import { onMount } from "svelte";
  import { toast } from "svelte-sonner";
  import { api } from "$lib/api";
  import DataTable from "$lib/components/ui/DataTable.svelte";

  let orders = $state<any[]>([]);
  let loading = $state(true);
  let filterStatus = $state("");

  const columns = [
    { key: "order_number", label: "Order" },
    { key: "user_id", label: "Customer" },
    { key: "items", label: "Items" },
    { key: "total_price", label: "Total" },
    { key: "status", label: "Status" },
  ];

  let filteredOrders = $derived(
    filterStatus
      ? orders.filter((o) => o.status === filterStatus)
      : orders
  );

   onMount(async () => {
     try {
       orders = await api.staffGetOrders();
     } catch (err: any) {
       toast.error(err.message || "Failed to load orders");
     } finally {
       loading = false;
     }
   });

  async function updateStatus(orderId: number, status: string) {
    try {
      const updated = await api.staffUpdateOrderStatus(orderId, status);
      orders = orders.map((o) => (o.id === orderId ? updated : o));
      toast.success("Order status updated");
    } catch (err: any) {
      toast.error(err.message);
    }
  }

  function statusColor(status: string) {
    const colors: Record<string, string> = { pending: "text-yellow-400", confirmed: "text-blue-400", preparing: "text-flame-orange", ready: "text-green-400", delivered: "text-green-400", completed: "text-green-400", cancelled: "text-red-400" };
    return colors[status] || "text-muted-gray";
  }
</script>

<div class="mb-6">
  <h1 class="font-headline-h2 text-headline-h2 text-ivory-white">Orders Management</h1>
  <p class="text-muted-gray text-sm mt-1">View and update order status</p>
</div>

<div class="flex gap-2 mb-6 flex-wrap">
  {#each ["", "pending", "confirmed", "preparing", "ready", "delivered", "completed", "cancelled"] as s}
    <button
      onclick={() => { filterStatus = s; }}
      class={filterStatus === s
        ? "bg-flame-orange text-ivory-white px-4 py-2 rounded-full text-sm font-bold cursor-pointer"
        : "bg-surface-card text-muted-gray hover:text-ivory-white px-4 py-2 rounded-full text-sm border border-deep-border cursor-pointer"}
    >
      {s || "All"}
    </button>
  {/each}
</div>

<div class="bg-surface-card rounded-2xl border border-deep-border p-6">
  <DataTable {columns} rows={filteredOrders} {loading} emptyMessage="No orders found">
    {#snippet cell({ col, row })}
      {#if col.key === "status"}
        <span class={statusColor(row.status)}>{row.status}</span>
      {:else if col.key === "total_price"}
        <span class="text-ivory-white">${Number(row.total_price).toFixed(2)}</span>
      {:else if col.key === "items"}
        <span class="text-muted-gray">{row.items?.length || 0}</span>
      {:else if col.key === "user_id"}
        <span class="text-ivory-white">{row.user_id}</span>
      {:else}
        <span class="text-ivory-white font-medium">{row[col.key]}</span>
      {/if}
    {/snippet}
    {#snippet actions({ row })}
      <div class="flex items-center justify-end gap-2">
        {#if row.status === "pending"}
          <button onclick={() => updateStatus(row.id, "confirmed")} class="text-blue-400 hover:text-blue-300 text-xs font-medium cursor-pointer">Confirm</button>
          <button onclick={() => updateStatus(row.id, "cancelled")} class="text-red-400 hover:text-red-300 text-xs font-medium cursor-pointer">Cancel</button>
        {:else if row.status === "confirmed"}
          <button onclick={() => updateStatus(row.id, "preparing")} class="text-flame-orange hover:text-flame-hover text-xs font-medium cursor-pointer">Preparing</button>
          <button onclick={() => updateStatus(row.id, "cancelled")} class="text-red-400 hover:text-red-300 text-xs font-medium cursor-pointer">Cancel</button>
        {:else if row.status === "preparing"}
          <button onclick={() => updateStatus(row.id, "ready")} class="text-green-400 hover:text-green-300 text-xs font-medium cursor-pointer">Ready</button>
        {:else if row.status === "ready"}
          <button onclick={() => updateStatus(row.id, "delivered")} class="text-green-400 hover:text-green-300 text-xs font-medium cursor-pointer">Delivered</button>
        {:else if row.status === "delivered"}
          <button onclick={() => updateStatus(row.id, "completed")} class="text-green-400 hover:text-green-300 text-xs font-medium cursor-pointer">Complete</button>
        {:else}
          <span class="text-muted-gray text-xs">-</span>
        {/if}
      </div>
    {/snippet}
  </DataTable>
</div>
