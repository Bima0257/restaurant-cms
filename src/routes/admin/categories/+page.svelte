<script lang="ts">
  import { onMount } from "svelte";
  import { Plus, Pencil, Trash2, X, Loader2 } from "@lucide/svelte";
  import { toast } from "svelte-sonner";
  import { confirmAction } from "$lib/utils/confirm";
  import { api } from "$lib/api";
  import SectionHeading from "$lib/components/ui/SectionHeading.svelte";
  import ImageUpload from "$lib/components/ui/ImageUpload.svelte";

  let categories = $state<any[]>([]);
  let loading = $state(true);
  let showModal = $state(false);
  let editing = $state<any>(null);
  let saving = $state(false);

  let form = $state({ name: "", slug: "", description: "", image_url: "", is_active: true });

  onMount(() => { load(); });

  async function load() {
    loading = true;
    try {
      categories = await api.adminListCategories();
    } catch (err: any) {
      toast.error(err.message || "Failed to load categories");
    } finally {
      loading = false;
    }
  }

  function resetForm() {
    form = { name: "", slug: "", description: "", image_url: "", is_active: true };
    editing = null;
  }

  function openCreate() {
    resetForm();
    showModal = true;
  }

  function openEdit(cat: any) {
    form = { name: cat.name, slug: cat.slug, description: cat.description || "", image_url: cat.image_url || "", is_active: cat.is_active };
    editing = cat;
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
        await api.adminUpdateCategory(editing.id, {
          name: form.name,
          slug: form.slug,
          description: form.description || undefined,
          is_active: form.is_active,
        });
        toast.success("Category updated");
      } else {
        await api.adminCreateCategory(form);
        toast.success("Category created");
      }
      showModal = false;
      resetForm();
      await load();
    } catch (err: any) {
      toast.error(err.message);
    } finally {
      saving = false;
    }
  }

  async function deleteCat(cat: any) {
    const confirmed = await confirmAction({
      title: "Delete Category",
      message: `Are you sure you want to delete "${cat.name}"?`,
      confirmLabel: "Delete",
      variant: "danger",
    });
    if (!confirmed) return;
    try {
      await api.adminDeleteCategory(cat.id);
      categories = categories.filter((c) => c.id !== cat.id);
      toast.success("Category deleted");
    } catch (err: any) {
      toast.error(err.message);
    }
  }
</script>

<div class="flex items-center justify-between mb-8">
  <SectionHeading prefix="Categories" highlight="Management" />
  <button onclick={openCreate} class="bg-flame-orange hover:bg-flame-hover text-ivory-white px-5 py-2.5 rounded-full font-bold text-sm flex items-center gap-2 transition-all cursor-pointer">
    <Plus size={16} />
    Add Category
  </button>
</div>

{#if loading}
  <div class="bg-surface-card rounded-2xl border border-deep-border p-12 text-center">
    <Loader2 size={24} class="animate-spin text-muted-gray mx-auto" />
    <p class="text-muted-gray text-sm mt-2">Loading...</p>
  </div>
{:else if categories.length === 0}
  <div class="bg-surface-card rounded-2xl border border-deep-border p-12 text-center">
    <p class="text-muted-gray">No categories yet</p>
  </div>
{:else}
  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
    {#each categories as cat}
      <div class="bg-surface-card rounded-2xl border border-deep-border p-6 hover:-translate-y-1 transition-transform duration-300">
        <div class="flex items-start justify-between mb-4">
          <div>
            <h4 class="font-headline-h3 text-headline-h3 text-ivory-white">{cat.name}</h4>
            <p class="text-muted-gray text-xs mt-1">/{cat.slug}</p>
            {#if cat.description}
              <p class="text-muted-gray text-xs mt-1 line-clamp-2">{cat.description}</p>
            {/if}
          </div>
          <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border {cat.is_active ? 'bg-green-500/10 text-green-400 border-green-500/20' : 'bg-red-500/10 text-red-400 border-red-500/20'}">
            {cat.is_active ? "Active" : "Inactive"}
          </span>
        </div>
        <div class="flex items-center justify-between pt-3 border-t border-deep-border">
          <span class="text-muted-gray text-xs">Sort: {cat.sort_order}</span>
          <div class="flex gap-1">
            <button onclick={() => openEdit(cat)} class="p-1.5 rounded-lg hover:bg-flame-orange/10 text-muted-gray hover:text-flame-orange transition-colors cursor-pointer" title="Edit">
              <Pencil size={14} />
            </button>
            <button onclick={() => deleteCat(cat)} class="p-1.5 rounded-lg hover:bg-red-500/10 text-muted-gray hover:text-red-400 transition-colors cursor-pointer" title="Delete">
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
    <div class="bg-surface-card rounded-3xl p-6 w-full max-w-md" onclick={(e: Event) => e.stopPropagation()} onkeydown={() => {}}>
      <div class="flex items-center justify-between mb-6">
        <h2 class="text-ivory-white font-bold text-lg">{editing ? "Edit" : "Create"} Category</h2>
        <button onclick={() => { showModal = false; resetForm(); }} class="p-1 rounded-lg hover:bg-surface-charcoal text-muted-gray hover:text-ivory-white transition-colors cursor-pointer"><X size={18} /></button>
      </div>
      <div class="flex flex-col gap-4">
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label for="c-name" class="block text-sm text-muted-gray mb-1">Name</label>
            <input id="c-name" class="w-full bg-surface-charcoal border border-deep-border rounded-xl px-4 py-3 text-sm focus:border-flame-orange outline-none text-ivory-white" placeholder="Category name" bind:value={form.name} oninput={onNameChange} />
          </div>
          <div>
            <label for="c-slug" class="block text-sm text-muted-gray mb-1">Slug</label>
            <input id="c-slug" class="w-full bg-surface-charcoal border border-deep-border rounded-xl px-4 py-3 text-sm focus:border-flame-orange outline-none text-ivory-white" placeholder="category-slug" bind:value={form.slug} />
          </div>
        </div>
        <div>
          <label for="c-desc" class="block text-sm text-muted-gray mb-1">Description</label>
          <textarea id="c-desc" class="w-full bg-surface-charcoal border border-deep-border rounded-xl px-4 py-3 text-sm focus:border-flame-orange outline-none text-ivory-white min-h-[80px]" placeholder="Description (optional)" bind:value={form.description}></textarea>
        </div>
        <div>
          <ImageUpload
            currentUrl={form.image_url}
            onUpload={(url: string) => form.image_url = url}
            label="Image"
          />
        </div>
        <div>
          <label for="c-status" class="block text-sm text-muted-gray mb-1">Status</label>
          <select id="c-status" class="w-full bg-surface-charcoal border border-deep-border rounded-xl px-4 py-3 text-sm focus:border-flame-orange outline-none text-ivory-white cursor-pointer" bind:value={form.is_active}>
            <option value={true}>Active</option>
            <option value={false}>Inactive</option>
          </select>
        </div>
        <div class="flex gap-3 mt-2">
          <button onclick={() => { showModal = false; resetForm(); }} class="flex-1 bg-surface-charcoal hover:bg-deep-border text-ivory-white py-3 rounded-full font-bold text-sm transition-all cursor-pointer">Cancel</button>
          <button onclick={save} disabled={saving || !form.name || !form.slug} class="flex-1 bg-flame-orange hover:bg-flame-hover text-ivory-white py-3 rounded-full font-bold text-sm transition-all cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed">
            {#if saving}<Loader2 size={16} class="animate-spin mx-auto" />{:else}{editing ? "Update" : "Create"}{/if}
          </button>
        </div>
      </div>
    </div>
  </div>
{/if}
