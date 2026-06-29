<script lang="ts">
  import { onMount } from "svelte";
  import { goto } from "$app/navigation";
  import { Plus, Search } from "@lucide/svelte";
  import { api } from "$lib/api";
  import { auth } from "$lib/stores/auth";
  import { get } from "svelte/store";

  let categories = $state<any[]>([]);
  let menuItems = $state<any[]>([]);
  let activeCategory = $state<string | null>(null);
  let loading = $state(true);
  let searchQuery = $state("");

  let filteredItems = $derived(
    menuItems.filter((item) => {
      const matchesCategory = !activeCategory || item.category_slug === activeCategory || item.category?.slug === activeCategory;
      const matchesSearch = !searchQuery || item.name.toLowerCase().includes(searchQuery.toLowerCase()) || (item.description || "").toLowerCase().includes(searchQuery.toLowerCase());
      return matchesCategory && matchesSearch;
    })
  );

  onMount(async () => {
    if (!get(auth)) {
      goto("/auth/login");
      return;
    }
    try {
      const [fetchedMenu, fetchedCategories] = await Promise.all([
        api.getMenu(),
        api.getCategories(),
      ]);
      menuItems = fetchedMenu;
      categories = fetchedCategories;
    } catch { /* empty state handles this */ }
    finally {
      loading = false;
    }
  });
</script>

<!-- Header -->
<div class="mb-8">
  <h1 class="font-headline-h1 text-headline-h1 text-ivory-white mb-1">Menu</h1>
  <p class="text-muted-gray text-body-lg">Browse our selection of premium dishes.</p>
</div>

<!-- Search & Filter Bar -->
<div class="flex flex-col sm:flex-row gap-4 mb-6">
  <div class="relative flex-1 max-w-md">
    <Search size={18} class="absolute left-4 top-1/2 -translate-y-1/2 text-muted-gray" />
    <input
      type="text"
      placeholder="Search menu..."
      bind:value={searchQuery}
      class="w-full bg-surface-charcoal border border-deep-border rounded-full pl-11 pr-5 py-3 text-sm text-ivory-white placeholder:text-muted-gray focus:border-flame-orange focus:ring-0 outline-none"
    />
  </div>
</div>

<!-- Category Tabs -->
<div class="flex flex-wrap gap-3 mb-8">
  <button
    onclick={() => activeCategory = null}
    class={"px-5 py-2 rounded-full text-sm font-bold transition-all cursor-pointer " + (!activeCategory
      ? "bg-flame-orange text-ivory-white"
      : "bg-surface-charcoal border border-deep-border text-muted-gray hover:text-ivory-white hover:border-flame-orange")}
  >
    All
  </button>
  {#each categories as cat}
    <button
      onclick={() => activeCategory = cat.slug}
      class={"px-5 py-2 rounded-full text-sm font-bold transition-all cursor-pointer " + (activeCategory === cat.slug
        ? "bg-flame-orange text-ivory-white"
        : "bg-surface-charcoal border border-deep-border text-muted-gray hover:text-ivory-white hover:border-flame-orange")}
    >
      {cat.name}
    </button>
  {/each}
</div>

<!-- Menu Grid -->
{#if loading}
  <div class="flex items-center justify-center min-h-[40vh]">
    <p class="text-muted-gray">Loading menu...</p>
  </div>
{:else if filteredItems.length === 0}
  <div class="flex flex-col items-center justify-center min-h-[40vh] gap-4">
    <p class="text-muted-gray text-lg">No menu items found.</p>
    <button
      onclick={() => { activeCategory = null; searchQuery = ""; }}
      class="text-flame-orange font-bold text-sm hover:underline cursor-pointer"
    >
      Clear filters
    </button>
  </div>
{:else}
  <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
    {#each filteredItems as item}
      <div class="bg-surface-card rounded-[1.5rem] p-4 border border-deep-border hover:translate-y-[-4px] transition-all duration-300 group">
        <div class="relative rounded-xl overflow-hidden aspect-square mb-4">
          <img
            class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
            alt={item.name}
            src={item.image_url || "https://placehold.co/400x400/1C1C1C/A0A0A0?text=WorldPlate"}
          />
          <div class="absolute top-3 right-3 bg-surface/80 backdrop-blur-md px-2 py-1 rounded-lg text-xs font-bold text-flame-orange">
            {item.rating || "4.9"} ★
          </div>
        </div>
        <h4 class="font-headline-h3 text-headline-h3 text-ivory-white mb-1">{item.name}</h4>
        <p class="text-xs text-muted-gray mb-4 line-clamp-2">{item.description || ""}</p>
        <div class="flex items-center justify-between">
          <span class="font-label-price text-label-price text-ivory-white">${Number(item.price).toFixed(2)}</span>
          <button class="w-10 h-10 bg-surface-charcoal border border-deep-border rounded-full flex items-center justify-center text-flame-orange hover:bg-flame-orange hover:text-white transition-all duration-300 cursor-pointer">
            <Plus size={18} />
          </button>
        </div>
      </div>
    {/each}
  </div>
{/if}