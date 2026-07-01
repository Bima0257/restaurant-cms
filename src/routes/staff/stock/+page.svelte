<script lang="ts">
  import { onMount } from "svelte";
  import { PackagePlus, Plus, Minus, X } from "@lucide/svelte";
  import { toast } from "svelte-sonner";
  import { api } from "$lib/api";
  import DataTable from "$lib/components/ui/DataTable.svelte";

  let ingredients = $state<any[]>([]);
  let loading = $state(true);
  let search = $state("");

  let showTransactionModal = $state(false);
  let transactionMode = $state<"in" | "adjust">("in");
  let selectedIngredient = $state<any>(null);
  let transactionQty = $state<number>(0);
  let transactionNotes = $state("");
  let submitting = $state(false);

  const columns = [
    { key: "name", label: "Name" },
    { key: "sku", label: "SKU" },
    { key: "unit", label: "Unit" },
    { key: "stock_qty", label: "Stock" },
    { key: "min_stock", label: "Min Stock" },
    { key: "status", label: "Status" },
  ];

  async function loadStock() {
    loading = true;
    try {
      ingredients = await api.staffCheckStock();
    } catch (err: any) {
      toast.error(err.message || "Failed to load stock data");
    } finally {
      loading = false;
    }
  }

  onMount(loadStock);

  let filtered = $derived(
    search
      ? ingredients.filter(
          (i) =>
            i.name.toLowerCase().includes(search.toLowerCase()) ||
            i.sku.toLowerCase().includes(search.toLowerCase())
        )
      : ingredients
  );

  function openStockIn(ingredient: any) {
    selectedIngredient = ingredient;
    transactionMode = "in";
    transactionQty = 0;
    transactionNotes = "";
    showTransactionModal = true;
  }

  function openAdjust(ingredient: any) {
    selectedIngredient = ingredient;
    transactionMode = "adjust";
    transactionQty = 0;
    transactionNotes = "";
    showTransactionModal = true;
  }

  function closeModal() {
    showTransactionModal = false;
    selectedIngredient = null;
  }

  async function handleSubmit() {
    if (!selectedIngredient) return;
    if (transactionMode === "in" && transactionQty <= 0) return;
    if (transactionMode === "adjust" && transactionQty === 0) return;
    submitting = true;
    try {
      if (transactionMode === "in") {
        await api.staffStockIn({ ingredient_id: selectedIngredient.id, qty: transactionQty, notes: transactionNotes || undefined });
        toast.success(`Stock-in ${selectedIngredient.name}: +${transactionQty}`);
      } else {
        await api.staffAdjustStock({ ingredient_id: selectedIngredient.id, qty: transactionQty, notes: transactionNotes || undefined });
        toast.success(`Stock adjusted for ${selectedIngredient.name}`);
      }
      closeModal();
      await loadStock();
    } catch (err: any) {
      toast.error(err.message || "Transaction failed");
    } finally {
      submitting = false;
    }
  }
</script>

<div class="mb-6">
  <h1 class="font-headline-h2 text-headline-h2 text-ivory-white">Stock Check</h1>
  <p class="text-muted-gray text-sm mt-1">Manage ingredient stock levels</p>
</div>

<input
  class="w-full max-w-md bg-surface-charcoal border border-deep-border rounded-xl px-4 py-3 text-sm focus:border-flame-orange focus:ring-0 outline-none text-ivory-white mb-6"
  placeholder="Search ingredients..."
  bind:value={search}
/>

<div class="bg-surface-card rounded-2xl border border-deep-border p-6">
  <DataTable {columns} rows={filtered} {loading} emptyMessage="No ingredients found">
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
    {#snippet actions({ row })}
      <div class="flex items-center justify-end gap-2">
        <button
          onclick={() => openStockIn(row)}
          class="flex items-center gap-1 px-2.5 py-1.5 rounded-lg text-xs font-medium text-flame-orange hover:bg-flame-orange/10 transition-colors cursor-pointer"
        >
          <Plus size={14} />
          Stock In
        </button>
        <button
          onclick={() => openAdjust(row)}
          class="flex items-center gap-1 px-2.5 py-1.5 rounded-lg text-xs font-medium text-muted-gray hover:text-ivory-white hover:bg-surface-charcoal transition-colors cursor-pointer"
        >
          <Minus size={14} />
          Adjust
        </button>
      </div>
    {/snippet}
  </DataTable>
</div>

{#if showTransactionModal && selectedIngredient}
  <div
    class="fixed inset-0 bg-black/60 flex items-center justify-center z-50 p-4"
    onclick={() => closeModal()}
    onkeydown={(e) => { if (e.key === "Escape") closeModal(); }}
    role="dialog"
    tabindex="0"
    aria-label="Stock transaction dialog"
  >
    <div
      class="bg-surface-card rounded-3xl p-6 w-full max-w-md border border-deep-border"
      onclick={(e) => e.stopPropagation()}
    >
      <div class="flex items-center justify-between mb-6">
        <h3 class="font-headline-h3 text-headline-h3 text-ivory-white">
          {transactionMode === "in" ? "Stock In" : "Adjust Stock"}
        </h3>
        <button onclick={() => closeModal()} class="text-muted-gray hover:text-ivory-white transition-colors cursor-pointer">
          <X size={20} />
        </button>
      </div>

      <div class="mb-4">
        <p class="text-sm text-muted-gray mb-1">Ingredient</p>
        <p class="text-ivory-white font-bold">{selectedIngredient.name}</p>
        <p class="text-xs text-muted-gray">SKU: {selectedIngredient.sku} | Current stock: {Number(selectedIngredient.stock_qty).toFixed(2)} {selectedIngredient.unit}</p>
      </div>

      <div class="space-y-4">
        <div>
          <label class="text-sm text-muted-gray block mb-1">
            {transactionMode === "in" ? "Quantity to add" : "Adjustment quantity"}
          </label>
          <input
            type="number"
            step="0.01"
            bind:value={transactionQty}
            class="w-full bg-surface-charcoal border border-deep-border rounded-xl px-4 py-3 text-sm text-ivory-white focus:border-flame-orange focus:ring-0 outline-none"
            placeholder="0.00"
          />
          {#if transactionMode === "adjust"}
            <p class="text-xs text-muted-gray mt-1">Use positive value to increase, negative to decrease.</p>
          {/if}
        </div>
        <div>
          <label class="text-sm text-muted-gray block mb-1">Notes (optional)</label>
          <input
            type="text"
            bind:value={transactionNotes}
            class="w-full bg-surface-charcoal border border-deep-border rounded-xl px-4 py-3 text-sm text-ivory-white focus:border-flame-orange focus:ring-0 outline-none"
            placeholder="e.g. Delivery from supplier"
          />
        </div>
      </div>

      <div class="flex gap-3 mt-6">
        <button
          onclick={() => closeModal()}
          class="flex-1 px-4 py-3 rounded-xl border border-deep-border text-muted-gray hover:text-ivory-white transition-colors cursor-pointer"
        >
          Cancel
        </button>
        <button
          onclick={handleSubmit}
          disabled={submitting || (transactionMode === "in" && transactionQty <= 0) || (transactionMode === "adjust" && transactionQty === 0)}
          class="flex-1 px-4 py-3 rounded-xl bg-flame-orange text-ivory-white font-bold hover:bg-flame-hover disabled:opacity-50 disabled:cursor-not-allowed transition-colors cursor-pointer"
        >
          {submitting ? "Processing..." : transactionMode === "in" ? "Stock In" : "Adjust"}
        </button>
      </div>
    </div>
  </div>
{/if}
