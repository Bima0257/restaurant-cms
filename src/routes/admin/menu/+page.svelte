<script lang="ts">
  import { onMount } from "svelte";
  import { Plus, Pencil, Trash2, X, Loader2 } from "@lucide/svelte";
  import { toast } from "svelte-sonner";
  import { confirmAction } from "$lib/utils/confirm";
  import { api } from "$lib/api";
  import SectionHeading from "$lib/components/ui/SectionHeading.svelte";
  import ImageUpload from "$lib/components/ui/ImageUpload.svelte";

  let menuItems = $state<any[]>([]);
  let categories = $state<any[]>([]);
  let loading = $state(true);
  let showModal = $state(false);
  let editing = $state<any>(null);
  let saving = $state(false);

  let form = $state({
    name: "",
    slug: "",
    category_id: 0,
    description: "",
    price: 0,
    image_url: "",
    is_available: true,
  });

  onMount(async () => {
    await Promise.all([loadMenu(), loadCategories()]);
  });

  async function loadMenu() {
    loading = true;
    try {
      menuItems = await api.adminListMenu();
    } catch (err: any) {
      toast.error(err.message || "Failed to load menu");
    } finally {
      loading = false;
    }
  }

  async function loadCategories() {
    try {
      categories = await api.adminListCategories();
    } catch { /* ignore */ }
  }

  function resetForm() {
    form = { name: "", slug: "", category_id: categories[0]?.id || 0, description: "", price: 0, image_url: "", is_available: true };
    editing = null;
  }

  function openCreate() {
    resetForm();
    form.category_id = categories[0]?.id || 0;
    showModal = true;
  }

  function openEdit(item: any) {
    form = {
      name: item.name,
      slug: item.slug,
      category_id: item.category_id,
      description: item.description || "",
      price: item.price,
      image_url: item.image_url || "",
      is_available: item.is_available,
    };
    editing = item;
    showModal = true;
  }

  function generateSlug(name: string) {
    return name.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
  }

  function onNameChange() {
    if (!editing) form.slug = generateSlug(form.name);
  }

  async function save() {
    saving = true;
    try {
      if (editing) {
        await api.adminUpdateMenuItem(editing.id, {
          name: form.name,
          slug: form.slug,
          category_id: form.category_id,
          description: form.description || undefined,
          price: form.price,
          image_url: form.image_url || undefined,
          is_available: form.is_available,
        });
        toast.success("Menu item updated");
      } else {
        await api.adminCreateMenuItem(form);
        toast.success("Menu item created");
      }
      showModal = false;
      resetForm();
      await loadMenu();
    } catch (err: any) {
      toast.error(err.message);
    } finally {
      saving = false;
    }
  }

  async function deleteItem(item: any) {
    const confirmed = await confirmAction({
      title: "Delete Menu Item",
      message: `Are you sure you want to delete "${item.name}"?`,
      confirmLabel: "Delete",
      variant: "danger",
    });
    if (!confirmed) return;
    try {
      await api.adminDeleteMenuItem(item.id);
      menuItems = menuItems.filter((i) => i.id !== item.id);
      toast.success("Menu item deleted");
    } catch (err: any) {
      toast.error(err.message);
    }
  }

  function formatPrice(price: number) {
    return `$${Number(price).toFixed(2)}`;
  }
</script>

<div class="flex items-center justify-between mb-8">
  <SectionHeading prefix="Menu" highlight="Management" />
  <button onclick={openCreate} class="bg-flame-orange hover:bg-flame-hover text-ivory-white px-5 py-2.5 rounded-full font-bold text-sm flex items-center gap-2 transition-all cursor-pointer">
    <Plus size={16} />
    Add Item
  </button>
</div>

{#if loading}
  <div class="bg-surface-card rounded-2xl border border-deep-border p-12 text-center">
    <Loader2 size={24} class="animate-spin text-muted-gray mx-auto" />
    <p class="text-muted-gray text-sm mt-2">Loading...</p>
  </div>
{:else if menuItems.length === 0}
  <div class="bg-surface-card rounded-2xl border border-deep-border p-12 text-center">
    <p class="text-muted-gray">No menu items yet</p>
  </div>
{:else}
  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
    {#each menuItems as item}
      <div class="bg-surface-card rounded-2xl border border-deep-border p-6 hover:-translate-y-1 transition-transform duration-300">
        <div class="flex items-start gap-4 mb-4">
          {#if item.image_url}
            <img src={item.image_url} alt={item.name} class="w-16 h-16 rounded-xl object-cover flex-shrink-0" />
          {:else}
            <div class="w-16 h-16 rounded-xl bg-surface-charcoal flex items-center justify-center flex-shrink-0">
              <span class="text-2xl text-muted-gray">{item.name.charAt(0)}</span>
            </div>
          {/if}
          <div class="flex-1 min-w-0">
            <h4 class="font-headline-h3 text-headline-h3 text-ivory-white truncate">{item.name}</h4>
            <p class="text-muted-gray text-xs mt-0.5">{item.category_name || "Uncategorized"}</p>
            <p class="text-flame-orange font-bold mt-1">{formatPrice(item.price)}</p>
          </div>
        </div>
        <div class="flex items-center justify-between pt-3 border-t border-deep-border">
          <span class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-medium border {item.is_available ? 'bg-green-500/10 text-green-400 border-green-500/20' : 'bg-red-500/10 text-red-400 border-red-500/20'}">
            <span class="w-1.5 h-1.5 rounded-full currentColor"></span>
            {item.is_available ? "Available" : "Unavailable"}
          </span>
          <div class="flex gap-1">
            <button onclick={() => openEdit(item)} class="p-1.5 rounded-lg hover:bg-flame-orange/10 text-muted-gray hover:text-flame-orange transition-colors cursor-pointer" title="Edit">
              <Pencil size={14} />
            </button>
            <button onclick={() => deleteItem(item)} class="p-1.5 rounded-lg hover:bg-red-500/10 text-muted-gray hover:text-red-400 transition-colors cursor-pointer" title="Delete">
              <Trash2 size={14} />
            </button>
          </div>
        </div>
      </div>
    {/each}
  </div>
{/if}

<!-- Create/Edit Modal -->
{#if showModal}
  <div class="fixed inset-0 bg-black/60 flex items-center justify-center z-[9999] p-4" onclick={() => { showModal = false; resetForm(); }} onkeydown={(e) => { if (e.key === "Escape") { showModal = false; resetForm(); } }} role="dialog" aria-modal="true" tabindex="-1">
    <div class="bg-surface-card rounded-3xl p-6 w-full max-w-lg" onclick={(e: Event) => e.stopPropagation()} onkeydown={() => {}}>
      <div class="flex items-center justify-between mb-6">
        <h2 class="text-ivory-white font-bold text-lg">{editing ? "Edit" : "Create"} Menu Item</h2>
        <button onclick={() => { showModal = false; resetForm(); }} class="p-1 rounded-lg hover:bg-surface-charcoal text-muted-gray hover:text-ivory-white transition-colors cursor-pointer"><X size={18} /></button>
      </div>
      <div class="flex flex-col gap-4">
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label for="m-name" class="block text-sm text-muted-gray mb-1">Name</label>
            <input id="m-name" class="w-full bg-surface-charcoal border border-deep-border rounded-xl px-4 py-3 text-sm focus:border-flame-orange outline-none text-ivory-white" placeholder="Item name" bind:value={form.name} oninput={onNameChange} />
          </div>
          <div>
            <label for="m-slug" class="block text-sm text-muted-gray mb-1">Slug</label>
            <input id="m-slug" class="w-full bg-surface-charcoal border border-deep-border rounded-xl px-4 py-3 text-sm focus:border-flame-orange outline-none text-ivory-white" placeholder="item-slug" bind:value={form.slug} />
          </div>
        </div>
        <div>
          <label for="m-category" class="block text-sm text-muted-gray mb-1">Category</label>
          <select id="m-category" class="w-full bg-surface-charcoal border border-deep-border rounded-xl px-4 py-3 text-sm focus:border-flame-orange outline-none text-ivory-white cursor-pointer" bind:value={form.category_id}>
            <option value={0}>Select category</option>
            {#each categories as cat}
              <option value={cat.id}>{cat.name}</option>
            {/each}
          </select>
        </div>
        <div>
          <label for="m-desc" class="block text-sm text-muted-gray mb-1">Description</label>
          <textarea id="m-desc" class="w-full bg-surface-charcoal border border-deep-border rounded-xl px-4 py-3 text-sm focus:border-flame-orange outline-none text-ivory-white min-h-[80px]" placeholder="Description" bind:value={form.description}></textarea>
        </div>
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label for="m-price" class="block text-sm text-muted-gray mb-1">Price ($)</label>
            <input id="m-price" class="w-full bg-surface-charcoal border border-deep-border rounded-xl px-4 py-3 text-sm focus:border-flame-orange outline-none text-ivory-white" type="number" step="0.01" min="0" bind:value={form.price} />
          </div>
          <div>
            <label for="m-status" class="block text-sm text-muted-gray mb-1">Status</label>
            <select id="m-status" class="w-full bg-surface-charcoal border border-deep-border rounded-xl px-4 py-3 text-sm focus:border-flame-orange outline-none text-ivory-white cursor-pointer" bind:value={form.is_available}>
              <option value={true}>Available</option>
              <option value={false}>Unavailable</option>
            </select>
          </div>
        </div>
        <div>
          <ImageUpload
            currentUrl={form.image_url}
            onUpload={(url: string) => form.image_url = url}
            label="Image"
          />
        </div>
        <div class="flex gap-3 mt-2">
          <button onclick={() => { showModal = false; resetForm(); }} class="flex-1 bg-surface-charcoal hover:bg-deep-border text-ivory-white py-3 rounded-full font-bold text-sm transition-all cursor-pointer">Cancel</button>
          <button onclick={save} disabled={saving || !form.name || !form.slug || !form.category_id || !form.price} class="flex-1 bg-flame-orange hover:bg-flame-hover text-ivory-white py-3 rounded-full font-bold text-sm transition-all cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed">
            {#if saving}<Loader2 size={16} class="animate-spin mx-auto" />{:else}{editing ? "Update" : "Create"}{/if}
          </button>
        </div>
      </div>
    </div>
  </div>
{/if}
