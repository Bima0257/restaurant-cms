<script lang="ts">
  import DataTable from "$lib/components/ui/DataTable.svelte";
  import SectionHeading from "$lib/components/ui/SectionHeading.svelte";

  const columns = [
    { key: "id", label: "Order ID" },
    { key: "customer", label: "Customer" },
    { key: "date", label: "Date" },
    { key: "items", label: "Items" },
    { key: "total", label: "Total" },
    { key: "status", label: "Status" },
  ];

  let orders = $state([
    { id: "#WP-1024", customer: "John Smith", date: "2025-06-22", items: "3", total: "$57.00", status: "Completed" },
    { id: "#WP-1023", customer: "Emily Davis", date: "2025-06-22", items: "2", total: "$43.00", status: "Preparing" },
    { id: "#WP-1022", customer: "Alex Johnson", date: "2025-06-21", items: "4", total: "$89.00", status: "Pending" },
    { id: "#WP-1021", customer: "Sarah Lee", date: "2025-06-21", items: "1", total: "$24.00", status: "Completed" },
    { id: "#WP-1020", customer: "Mike Brown", date: "2025-06-20", items: "2", total: "$38.00", status: "Delivered" },
    { id: "#WP-1019", customer: "Lisa Wang", date: "2025-06-20", items: "3", total: "$66.00", status: "Cancelled" },
    { id: "#WP-1018", customer: "Tom Hardy", date: "2025-06-19", items: "5", total: "$112.00", status: "Completed" },
  ]);

  function handleView(row: Record<string, any>) {
    console.log("View order:", row.id);
  }

  const statusColors: Record<string, string> = {
    Completed: "text-green-400",
    Preparing: "text-flame-orange",
    Pending: "text-yellow-400",
    Delivered: "text-blue-400",
    Cancelled: "text-red-400",
  };
</script>

<div class="mb-8">
  <SectionHeading prefix="Orders" highlight="Management" />
</div>

<div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
  {#each [
    { label: "Total Orders", value: "156", color: "text-flame-orange" },
    { label: "Pending", value: "4", color: "text-yellow-400" },
    { label: "Preparing", value: "8", color: "text-flame-orange" },
    { label: "Delivered", value: "132", color: "text-green-400" },
  ] as stat}
    <div class="bg-surface-card rounded-2xl p-4 border border-deep-border">
      <p class="text-muted-gray text-sm">{stat.label}</p>
      <p class="font-headline-h2 text-headline-h2 {stat.color} mt-1">{stat.value}</p>
    </div>
  {/each}
</div>

<div class="bg-surface-card rounded-2xl border border-deep-border p-6">
  <DataTable {columns} rows={orders} onRowClick={handleView}>
    {#snippet cell({ col, row })}
      {#if col.key === "status"}
        <span class={statusColors[row.status] || "text-muted-gray"}>{row.status}</span>
      {:else}
        <span class="text-ivory-white">{row[col.key as keyof typeof row]}</span>
      {/if}
    {/snippet}
  </DataTable>
</div>
