<script lang="ts">
  import { Plus } from "@lucide/svelte";
  import DataTable from "$lib/components/ui/DataTable.svelte";
  import SectionHeading from "$lib/components/ui/SectionHeading.svelte";

  const columns = [
    { key: "name", label: "Name" },
    { key: "category", label: "Category" },
    { key: "price", label: "Price" },
    { key: "status", label: "Status" },
  ];

  let menuItems = $state([
    { name: "Margherita Pizza", category: "Pizza", price: "$19.00", status: "Active" },
    { name: "Signature Burger", category: "Burgers", price: "$24.00", status: "Active" },
    { name: "Salmon Sushi Set", category: "Sushi", price: "$32.00", status: "Active" },
    { name: "Breakfast Specials", category: "Breakfast", price: "$99.00", status: "Active" },
    { name: "Ramen Bowl", category: "Noodles", price: "$28.00", status: "Inactive" },
    { name: "Wood-Fired Pizza", category: "Pizza", price: "$22.00", status: "Active" },
  ]);

  function handleEdit(row: Record<string, any>) {
    console.log("Edit:", row);
  }

  function handleDelete(row: Record<string, any>) {
    menuItems = menuItems.filter((item) => item.name !== row.name);
  }
</script>

<div class="flex items-center justify-between mb-8">
  <SectionHeading prefix="Menu" highlight="Management" />
  <button class="bg-flame-orange hover:bg-flame-hover text-ivory-white px-5 py-2.5 rounded-full font-bold text-sm flex items-center gap-2 transition-all cursor-pointer">
    <Plus size={16} />
    Add Item
  </button>
</div>

<div class="bg-surface-card rounded-2xl border border-deep-border p-6">
  <DataTable {columns} rows={menuItems} onEdit={handleEdit} onDelete={handleDelete} />
</div>
