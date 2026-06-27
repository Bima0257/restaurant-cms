<script lang="ts">
  import { Plus, Pencil, Trash2 } from "@lucide/svelte";
  import SectionHeading from "$lib/components/ui/SectionHeading.svelte";

  let categories = $state([
    { name: "Pizza", items: 8, slug: "pizza" },
    { name: "Burgers", items: 6, slug: "burgers" },
    { name: "Sushi", items: 5, slug: "sushi" },
    { name: "Breakfast", items: 4, slug: "breakfast" },
    { name: "Noodles", items: 7, slug: "noodles" },
    { name: "Desserts", items: 10, slug: "desserts" },
    { name: "Beverages", items: 8, slug: "beverages" },
  ]);
</script>

<div class="flex items-center justify-between mb-8">
  <SectionHeading prefix="Categories" highlight="Management" />
  <button class="bg-flame-orange hover:bg-flame-hover text-ivory-white px-5 py-2.5 rounded-full font-bold text-sm flex items-center gap-2 transition-all cursor-pointer">
    <Plus size={16} />
    Add Category
  </button>
</div>

<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
  {#each categories as cat}
    <div class="bg-surface-card rounded-2xl border border-deep-border p-6 hover:-translate-y-1 transition-transform duration-300">
      <div class="flex items-start justify-between mb-4">
        <div>
          <h4 class="font-headline-h3 text-headline-h3 text-ivory-white">{cat.name}</h4>
          <p class="text-muted-gray text-sm mt-1">{cat.items} items</p>
          <p class="text-muted-gray text-xs mt-1">/{cat.slug}</p>
        </div>
        <div class="flex gap-2">
          <button class="p-1.5 rounded-lg hover:bg-flame-orange/10 text-muted-gray hover:text-flame-orange transition-colors cursor-pointer">
            <Pencil size={14} />
          </button>
          <button class="p-1.5 rounded-lg hover:bg-red-500/10 text-muted-gray hover:text-red-400 transition-colors cursor-pointer">
            <Trash2 size={14} />
          </button>
        </div>
      </div>
    </div>
  {/each}
</div>
