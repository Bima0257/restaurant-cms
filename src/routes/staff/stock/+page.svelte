<script lang="ts">
  import { onMount } from "svelte";
  import { toast } from "svelte-sonner";
  import { api } from "$lib/api";
  import DataTable from "$lib/components/ui/DataTable.svelte";

  let ingredients = $state<any[]>([]);
  let loading = $state(true);
  let search = $state("");

  const columns = [
    { key: "name", label: "Name" },
    { key: "sku", label: "SKU" },
    { key: "unit", label: "Unit" },
    { key: "stock_qty", label: "Stock" },
    { key: "min_stock", label: "Min Stock" },
    { key: "status", label: "Status" },
  ];

   onMount(async () => {
     try {
       ingredients = await api.staffCheckStock();
     } catch (err: any) {
       toast.error(err.message || "Failed to load stock data");
     } finally {
       loading = false;
     }
   });

  let filtered = $derived(
    search
      ? ingredients.filter(
          (i) =>
            i.name.toLowerCase().includes(search.toLowerCase()) ||
            i.sku.toLowerCase().includes(search.toLowerCase())
        )
      : ingredients
  );
</script>

<div class="mb-6">
  <h1 class="font-headline-h2 text-headline-h2 text-ivory-white">Stock Check</h1>
  <p class="text-muted-gray text-sm mt-1">View current ingredient stock (read-only)</p>
</div>

<input
  class="w-full max-w-md bg-surface-charcoal border border-deep-border rounded-xl px-4 py-3 text-sm focus:border-flame-orange focus:ring-0 outline-none text-ivory-white mb-6"
  placeholder="Search ingredients..."
  bind:value={search}
/>

<div class="bg-surface-card rounded-2xl border border-deep-border p-6">
  <DataTable {columns} rows={filtered} {loading}>
    {#snippet cell({ col, row })}
      {#if col.key === "status"}
        {#if Number(row.stock_qty) <= 0}
          <span class="text-red-400 font-medium">Out of Stock</span>
        {:else if Number(row.stock_qty) <= Number(row.min_stock)}
          <span class="text-yellow-400 font-medium">Low Stock</span>
        {:else}
          <span class="text-green-400 font-medium">In Stock</span>
        {/if}
      {:else if col.key === "stock_qty"}
        <span class="text-ivory-white text-right block">{Number(row.stock_qty).toFixed(2)}</span>
      {:else if col.key === "min_stock"}
        <span class="text-muted-gray text-right block">{Number(row.min_stock).toFixed(2)}</span>
      {:else if col.key === "sku" || col.key === "unit"}
        <span class="text-muted-gray">{row[col.key]}</span>
      {:else}
        <span class="text-ivory-white">{row[col.key]}</span>
      {/if}
    {/snippet}
  </DataTable>
</div>
