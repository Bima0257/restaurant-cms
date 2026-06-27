<script lang="ts">
  import { ArrowLeft } from "@lucide/svelte";
  import { page } from "$app/stores";
  import SectionHeading from "$lib/components/ui/SectionHeading.svelte";

  const id = $page.url.pathname.split("/").pop();
</script>

<div class="mb-8">
  <a href="/admin/menu" class="inline-flex items-center gap-2 text-muted-gray hover:text-flame-orange transition-colors mb-4">
    <ArrowLeft size={16} />
    Back to Menu
  </a>
  <SectionHeading prefix="Edit" highlight="Menu Item" />
</div>

<div class="bg-surface-card rounded-2xl border border-deep-border p-6 max-w-2xl">
  <form class="flex flex-col gap-4">
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div>
        <label for="name" class="block text-sm text-muted-gray mb-1">Name</label>
        <input id="name"
          class="w-full bg-surface-charcoal border border-deep-border rounded-xl px-4 py-3 text-sm focus:border-flame-orange focus:ring-0 outline-none text-ivory-white"
          type="text"
          value="Item {id}"
        />
      </div>
      <div>
        <label for="category" class="block text-sm text-muted-gray mb-1">Category</label>
        <select id="category" class="w-full bg-surface-charcoal border border-deep-border rounded-xl px-4 py-3 text-sm focus:border-flame-orange focus:ring-0 outline-none text-ivory-white">
          <option>Pizza</option>
          <option>Burgers</option>
          <option>Sushi</option>
          <option>Noodles</option>
        </select>
      </div>
    </div>
    <div>
      <label for="description" class="block text-sm text-muted-gray mb-1">Description</label>
      <textarea id="description" class="w-full bg-surface-charcoal border border-deep-border rounded-xl px-4 py-3 text-sm focus:border-flame-orange focus:ring-0 outline-none text-ivory-white min-h-[100px]"></textarea>
    </div>
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div>
        <label for="price" class="block text-sm text-muted-gray mb-1">Price</label>
        <input id="price"
          class="w-full bg-surface-charcoal border border-deep-border rounded-xl px-4 py-3 text-sm focus:border-flame-orange focus:ring-0 outline-none text-ivory-white"
          type="text"
        />
      </div>
      <div>
        <label for="status" class="block text-sm text-muted-gray mb-1">Status</label>
        <select id="status" class="w-full bg-surface-charcoal border border-deep-border rounded-xl px-4 py-3 text-sm focus:border-flame-orange focus:ring-0 outline-none text-ivory-white">
          <option>Active</option>
          <option>Inactive</option>
        </select>
      </div>
    </div>
    <div>
      <label for="image" class="block text-sm text-muted-gray mb-1">Image URL</label>
      <input id="image"
        class="w-full bg-surface-charcoal border border-deep-border rounded-xl px-4 py-3 text-sm focus:border-flame-orange focus:ring-0 outline-none text-ivory-white"
        type="text"
      />
    </div>
    <button class="bg-flame-orange hover:bg-flame-hover text-ivory-white py-3 rounded-full font-bold transition-all cursor-pointer mt-2">
      Save Changes
    </button>
  </form>
</div>
