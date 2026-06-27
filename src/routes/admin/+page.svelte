<script lang="ts">
  import StatCard from "$lib/components/admin/StatCard.svelte";
  import DataTable from "$lib/components/ui/DataTable.svelte";
  import {
    UtensilsCrossed,
    ShoppingCart,
    DollarSign,
    Users,
    TrendingUp,
    TrendingDown,
  } from "@lucide/svelte";
  import SectionHeading from "$lib/components/ui/SectionHeading.svelte";

  const stats = [
    { title: "Total Menu Items", value: "48", icon: UtensilsCrossed, trend: "12%", trendUp: true },
    { title: "Total Orders", value: "156", icon: ShoppingCart, trend: "8%", trendUp: true },
    { title: "Revenue", value: "$12,480", icon: DollarSign, trend: "15%", trendUp: true },
    { title: "Customers", value: "284", icon: Users, trend: "3%", trendUp: false },
  ];

  const recentColumns = [
    { key: "id", label: "Order ID" },
    { key: "customer", label: "Customer" },
    { key: "items", label: "Items" },
    { key: "total", label: "Total" },
    { key: "status", label: "Status" },
  ];

  const recentOrders = [
    { id: "#WP-1024", customer: "John Smith", items: "3", total: "$57.00", status: "Completed" },
    { id: "#WP-1023", customer: "Emily Davis", items: "2", total: "$43.00", status: "Preparing" },
    { id: "#WP-1022", customer: "Alex Johnson", items: "4", total: "$89.00", status: "Pending" },
    { id: "#WP-1021", customer: "Sarah Lee", items: "1", total: "$24.00", status: "Completed" },
    { id: "#WP-1020", customer: "Mike Brown", items: "2", total: "$38.00", status: "Delivered" },
  ];

  const statusColors: Record<string, string> = {
    Completed: "text-green-400",
    Preparing: "text-flame-orange",
    Pending: "text-yellow-400",
    Delivered: "text-blue-400",
  };
</script>

<div class="mb-8">
  <SectionHeading prefix="Admin" highlight="Dashboard" />
</div>

<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
  {#each stats as stat}
    <StatCard {...stat} />
  {/each}
</div>

<div class="bg-surface-card rounded-2xl border border-deep-border p-6">
  <div class="flex items-center justify-between mb-6">
    <h3 class="font-headline-h3 text-headline-h3 text-ivory-white">Recent Orders</h3>
    <a href="/admin/orders" class="text-sm text-flame-orange hover:underline">View All</a>
  </div>
  <div class="overflow-x-auto">
    <DataTable columns={recentColumns} rows={recentOrders}>
      {#snippet cell({ col, row })}
        {#if col.key === "status"}
          <span class={statusColors[row.status] || "text-muted-gray"}>{row.status}</span>
        {:else}
          <span class="text-ivory-white">{row[col.key]}</span>
        {/if}
      {/snippet}
    </DataTable>
  </div>
</div>
