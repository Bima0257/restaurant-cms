<script lang="ts">
  import { CreditCard, MapPin, FileText } from "@lucide/svelte";
  import { goto } from "$app/navigation";
  import { onMount } from "svelte";
  import { toast } from "svelte-sonner";
  import { api } from "$lib/api";
  import { auth } from "$lib/stores/auth";
  import { get } from "svelte/store";

  let items = $state<any[]>([]);
  let paymentMethod = $state("cash");
  let deliveryAddress = $state("");
  let notes = $state("");
  let loading = $state(false);

   onMount(async () => {
    if (!get(auth)) {
      goto("/auth/login");
      return;
    }
    try {
      items = await api.getCart();
    } catch (err: any) {
      toast.error(err.message || "Failed to load cart");
    }
  });

  let total = $derived(items.reduce((sum, i) => sum + (i.subtotal || 0), 0));

  async function placeOrder(e: Event) {
    e.preventDefault();
    loading = true;
    try {
      const order = await api.createOrder({
        payment_method: paymentMethod,
        delivery_address: deliveryAddress || undefined,
        notes: notes || undefined,
      });
      goto(`/dashboard/orders/${order.id}`);
    } catch (err: any) {
      toast.error(err.message);
    } finally {
      loading = false;
    }
  }
</script>

<div class="pt-32 pb-20 px-gutter max-w-grid-max-width mx-auto">
  <h1 class="font-headline-h1 text-headline-h1 mb-8">Checkout</h1>

  <form class="grid grid-cols-1 lg:grid-cols-3 gap-8" onsubmit={placeOrder}>
    <div class="lg:col-span-2 space-y-6">

      <div class="bg-surface-card rounded-2xl border border-deep-border p-6">
        <h3 class="font-headline-h3 text-headline-h3 text-ivory-white mb-4 flex items-center gap-2">
          <CreditCard size={20} class="text-flame-orange" /> Payment Method
        </h3>
        <div class="flex gap-4">
          {#each ["cash", "transfer", "qris"] as method}
            <label class="flex items-center gap-2 bg-surface-charcoal rounded-xl px-4 py-3 border border-deep-border cursor-pointer hover:border-flame-orange transition-colors">
              <input type="radio" name="payment" value={method} bind:group={paymentMethod} class="text-flame-orange" />
              <span class="text-ivory-white text-sm capitalize">{method}</span>
            </label>
          {/each}
        </div>
      </div>

      <div class="bg-surface-card rounded-2xl border border-deep-border p-6">
        <h3 class="font-headline-h3 text-headline-h3 text-ivory-white mb-4 flex items-center gap-2">
          <MapPin size={20} class="text-flame-orange" /> Delivery Address
        </h3>
        <textarea
          class="w-full bg-surface-charcoal border border-deep-border rounded-xl px-4 py-3 text-sm focus:border-flame-orange focus:ring-0 outline-none text-ivory-white min-h-[80px]"
          placeholder="Enter your delivery address"
          bind:value={deliveryAddress}
        ></textarea>
      </div>

      <div class="bg-surface-card rounded-2xl border border-deep-border p-6">
        <h3 class="font-headline-h3 text-headline-h3 text-ivory-white mb-4 flex items-center gap-2">
          <FileText size={20} class="text-flame-orange" /> Order Notes
        </h3>
        <textarea
          class="w-full bg-surface-charcoal border border-deep-border rounded-xl px-4 py-3 text-sm focus:border-flame-orange focus:ring-0 outline-none text-ivory-white min-h-[80px]"
          placeholder="Any special requests?"
          bind:value={notes}
        ></textarea>
      </div>
    </div>

    <div class="bg-surface-card rounded-2xl border border-deep-border p-6 h-fit sticky top-24">
      <h3 class="font-headline-h3 text-headline-h3 text-ivory-white mb-4">Order Summary</h3>
      <div class="space-y-3 mb-4">
        {#each items as item}
          <div class="flex justify-between text-sm">
            <span class="text-muted-gray">{item.menu_item_name} x{item.qty}</span>
            <span class="text-ivory-white">${Number(item.subtotal).toFixed(2)}</span>
          </div>
        {/each}
      </div>
      <div class="border-t border-deep-border pt-4 flex justify-between text-ivory-white font-bold text-lg">
        <span>Total</span>
        <span>${total.toFixed(2)}</span>
      </div>
      <button disabled={loading || items.length === 0} class="w-full bg-flame-orange hover:bg-flame-hover text-ivory-white py-3 rounded-full font-bold transition-all mt-6 cursor-pointer disabled:opacity-50">
        {loading ? "Processing..." : "Place Order"}
      </button>
    </div>
  </form>
</div>
