<script lang="ts">
  import { Trash2, Minus, Plus, ShoppingCart } from "@lucide/svelte";
  import { goto } from "$app/navigation";
  import { onMount } from "svelte";
  import { toast } from "svelte-sonner";
  import { api } from "$lib/api";
  import { auth } from "$lib/stores/auth";
  import { get } from "svelte/store";

  let items = $state<any[]>([]);
  let loading = $state(true);

  onMount(async () => {
    if (!get(auth)) {
      goto("/auth/login");
      return;
    }
    try {
      items = await api.getCart();
    } catch (err: any) {
      toast.error(err.message || "Failed to load cart");
    } finally {
      loading = false;
    }
  });

  async function updateQty(id: number, qty: number) {
    if (qty < 1) return;
    try {
      const updated = await api.updateCart(id, { qty });
      items = items.map((i) => (i.id === id ? updated : i));
    } catch (err: any) {
      toast.error(err.message);
    }
  }

  async function removeItem(id: number) {
    try {
      await api.deleteCartItem(id);
      items = items.filter((i) => i.id !== id);
      toast.success("Item removed from cart");
    } catch (err: any) {
      toast.error(err.message);
    }
  }

  let total = $derived(items.reduce((sum, i) => sum + (i.subtotal || 0), 0));
</script>

<div class="mb-8">
  <h1 class="font-headline-h1 text-headline-h1 text-ivory-white flex items-center gap-3">
    <ShoppingCart size={28} class="text-flame-orange" />
    Your Cart
  </h1>
</div>

{#if loading}
  <div class="flex items-center justify-center min-h-[40vh]">
    <p class="text-muted-gray">Loading cart...</p>
  </div>
{:else if items.length === 0}
  <div class="flex flex-col items-center justify-center min-h-[40vh] gap-4">
    <div class="w-16 h-16 bg-surface-charcoal rounded-full flex items-center justify-center">
      <ShoppingCart size={32} class="text-muted-gray" />
    </div>
    <p class="text-muted-gray text-lg">Your cart is empty</p>
    <a href="/dashboard/menu" class="bg-flame-orange hover:bg-flame-hover text-ivory-white px-8 py-3 rounded-full font-bold text-sm transition-all">
      Browse Menu
    </a>
  </div>
{:else}
  <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
    <div class="lg:col-span-2 space-y-4">
      {#each items as item}
        <div class="bg-surface-card rounded-[1.5rem] border border-deep-border p-4 flex items-center gap-4">
          <img src={item.menu_item_image} alt={item.menu_item_name} class="w-20 h-20 rounded-xl object-cover shrink-0" />
          <div class="flex-1 min-w-0">
            <h4 class="font-headline-h3 text-headline-h3 text-ivory-white truncate">{item.menu_item_name}</h4>
            <p class="text-flame-orange font-bold">${Number(item.menu_item_price).toFixed(2)}</p>
          </div>
          <div class="flex items-center gap-2">
            <button onclick={() => updateQty(item.id, item.qty - 1)} class="w-8 h-8 rounded-full bg-surface-charcoal text-ivory-white flex items-center justify-center hover:bg-flame-orange transition-colors cursor-pointer">
              <Minus size={14} />
            </button>
            <span class="text-ivory-white font-bold w-8 text-center">{item.qty}</span>
            <button onclick={() => updateQty(item.id, item.qty + 1)} class="w-8 h-8 rounded-full bg-surface-charcoal text-ivory-white flex items-center justify-center hover:bg-flame-orange transition-colors cursor-pointer">
              <Plus size={14} />
            </button>
          </div>
          <p class="text-ivory-white font-bold w-20 text-right shrink-0">${Number(item.subtotal).toFixed(2)}</p>
          <button onclick={() => removeItem(item.id)} class="text-red-400 hover:text-red-300 transition-colors cursor-pointer shrink-0">
            <Trash2 size={18} />
          </button>
        </div>
      {/each}
    </div>
    <div class="bg-surface-card rounded-[1.5rem] border border-deep-border p-6 h-fit sticky top-24">
      <h3 class="font-headline-h3 text-headline-h3 text-ivory-white mb-4">Order Summary</h3>
      <div class="flex justify-between text-muted-gray mb-2">
        <span>Subtotal</span>
        <span>${total.toFixed(2)}</span>
      </div>
      <div class="border-t border-deep-border my-4 pt-4 flex justify-between text-ivory-white font-bold text-lg">
        <span>Total</span>
        <span>${total.toFixed(2)}</span>
      </div>
      <button onclick={() => goto("/checkout")} class="w-full bg-flame-orange hover:bg-flame-hover text-ivory-white py-3 rounded-full font-bold transition-all cursor-pointer">
        Proceed to Checkout
      </button>
    </div>
  </div>
{/if}