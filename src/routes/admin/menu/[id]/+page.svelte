<script lang="ts">
  import { onMount } from "svelte";
  import { ArrowLeft, Loader2 } from "@lucide/svelte";
  import { page } from "$app/stores";
  import { toast } from "svelte-sonner";
  import { api } from "$lib/api";
  import SectionHeading from "$lib/components/ui/SectionHeading.svelte";
  import ImageUpload from "$lib/components/ui/ImageUpload.svelte";

  const id = Number($page.params.id);
  let loading = $state(true);
  let saving = $state(false);
  let categories = $state<any[]>([]);

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
    try {
      const [item, cats] = await Promise.all([
        api.adminGetMenuItem(id),
        api.adminListCategories().catch(() => []),
      ]);
      form = {
        name: item.name,
        slug: item.slug,
        category_id: item.category_id,
        description: item.description || "",
        price: item.price,
        image_url: item.image_url || "",
        is_available: item.is_available,
      };
      categories = cats;
    } catch (err: any) {
      toast.error(err.message || "Failed to load menu item");
    } finally {
      loading = false;
    }
  });

  async function save() {
    saving = true;
    try {
      await api.adminUpdateMenuItem(id, {
        name: form.name,
        slug: form.slug,
        category_id: form.category_id,
        description: form.description || undefined,
        price: form.price,
        image_url: form.image_url || undefined,
        is_available: form.is_available,
      });
      toast.success("Menu item updated");
    } catch (err: any) {
      toast.error(err.message);
    } finally {
      saving = false;
    }
  }
</script>

<div class="mb-8">
  <a href="/admin/menu" class="inline-flex items-center gap-2 text-muted-gray hover:text-flame-orange transition-colors mb-4">
    <ArrowLeft size={16} />
    Back to Menu
  </a>
  <SectionHeading prefix="Edit" highlight="Menu Item" />
</div>

{#if loading}
  <div class="bg-surface-card rounded-2xl border border-deep-border p-12 text-center">
    <Loader2 size={24} class="animate-spin text-muted-gray mx-auto" />
    <p class="text-muted-gray text-sm mt-2">Loading...</p>
  </div>
{:else}
  <div class="bg-surface-card rounded-2xl border border-deep-border p-6 max-w-2xl">
    <form class="flex flex-col gap-4" onsubmit={(e) => { e.preventDefault(); save(); }}>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label for="edit-name" class="block text-sm text-muted-gray mb-1">Name</label>
          <input id="edit-name"
            class="w-full bg-surface-charcoal border border-deep-border rounded-xl px-4 py-3 text-sm focus:border-flame-orange outline-none text-ivory-white"
            type="text"
            bind:value={form.name}
          />
        </div>
        <div>
          <label for="edit-slug" class="block text-sm text-muted-gray mb-1">Slug</label>
          <input id="edit-slug"
            class="w-full bg-surface-charcoal border border-deep-border rounded-xl px-4 py-3 text-sm focus:border-flame-orange outline-none text-ivory-white"
            type="text"
            bind:value={form.slug}
          />
        </div>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label for="edit-category" class="block text-sm text-muted-gray mb-1">Category</label>
          <select id="edit-category" class="w-full bg-surface-charcoal border border-deep-border rounded-xl px-4 py-3 text-sm focus:border-flame-orange outline-none text-ivory-white cursor-pointer" bind:value={form.category_id}>
            <option value={0}>Select category</option>
            {#each categories as cat}
              <option value={cat.id}>{cat.name}</option>
            {/each}
          </select>
        </div>
        <div>
          <label for="edit-price" class="block text-sm text-muted-gray mb-1">Price ($)</label>
          <input id="edit-price"
            class="w-full bg-surface-charcoal border border-deep-border rounded-xl px-4 py-3 text-sm focus:border-flame-orange outline-none text-ivory-white"
            type="number" step="0.01" min="0"
            bind:value={form.price}
          />
        </div>
      </div>
      <div>
        <label for="edit-desc" class="block text-sm text-muted-gray mb-1">Description</label>
        <textarea id="edit-desc" class="w-full bg-surface-charcoal border border-deep-border rounded-xl px-4 py-3 text-sm focus:border-flame-orange outline-none text-ivory-white min-h-[100px]" bind:value={form.description}></textarea>
      </div>
      <div>
        <ImageUpload
          currentUrl={form.image_url}
          onUpload={(url: string) => form.image_url = url}
          label="Image"
        />
      </div>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label for="edit-status" class="block text-sm text-muted-gray mb-1">Status</label>
          <select id="edit-status" class="w-full bg-surface-charcoal border border-deep-border rounded-xl px-4 py-3 text-sm focus:border-flame-orange outline-none text-ivory-white cursor-pointer" bind:value={form.is_available}>
            <option value={true}>Available</option>
            <option value={false}>Unavailable</option>
          </select>
        </div>
      </div>
      <button type="submit" disabled={saving || !form.name || !form.slug || !form.category_id}
        class="bg-flame-orange hover:bg-flame-hover text-ivory-white py-3 rounded-full font-bold transition-all cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed mt-2">
        {#if saving}
          <Loader2 size={16} class="animate-spin mx-auto" />
        {:else}
          Save Changes
        {/if}
      </button>
    </form>
  </div>
{/if}
