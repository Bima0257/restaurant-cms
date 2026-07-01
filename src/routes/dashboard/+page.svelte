<script lang="ts">
  import { onMount } from "svelte";
  import { goto } from "$app/navigation";
  import { Plus, History, ShoppingCart, CookingPot, Stars, ReceiptText, ArrowRight } from "@lucide/svelte";
  import { toast } from "svelte-sonner";
  import { api } from "$lib/api";
  import { auth } from "$lib/stores/auth";
  import { get } from "svelte/store";

  let user = $derived(get(auth));

  let orders = $state<any[]>([]);
  let menuItems = $state<any[]>([]);
  let loading = $state(true);

  let activeOrder = $derived(orders.find((o) => o.status === "preparing" || o.status === "ready"));
  let lastOrder = $derived(orders.filter((o) => o.status === "delivered" || o.status === "completed").sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())[0]);
  let recentOrders = $derived(orders.slice(0, 3));

  onMount(async () => {
    if (!get(auth)) {
      goto("/auth/login");
      return;
    }
    try {
      const [fetchedOrders, fetchedMenu] = await Promise.all([
        api.getMyOrders(),
        api.getMenu(),
      ]);
      orders = fetchedOrders;
      menuItems = fetchedMenu;
    } catch { /* handled via empty states */ }
    finally {
      loading = false;
    }
  });

  function statusColor(status: string) {
    const colors: Record<string, string> = {
      pending: "text-yellow-400",
      confirmed: "text-blue-400",
      preparing: "text-flame-orange",
      ready: "text-green-400",
      delivered: "text-green-400",
      completed: "text-green-400",
      cancelled: "text-red-400",
    };
    return colors[status] || "text-muted-gray";
  }

  async function addToCart(item: any) {
    try {
      await api.addToCart({ menu_item_id: item.id, qty: 1 });
      toast.success(`${item.name} added to cart`);
    } catch (err: any) {
      toast.error(err.message);
    }
  }

  function copyPromoCode() {
    navigator.clipboard.writeText("WP-TRUFFLE-25");
    toast.success("Promo code copied!");
  }
</script>

{#if loading}
  <div class="flex items-center justify-center min-h-[60vh]">
    <p class="text-muted-gray">Loading your culinary dashboard...</p>
  </div>
{:else}
  <!-- Hero Section & Quick Reorder -->
  <section class="grid grid-cols-1 lg:grid-cols-3 gap-8 items-stretch">
    <div class="lg:col-span-2 bg-surface-charcoal rounded-[2rem] p-10 relative overflow-hidden flex flex-col justify-center min-h-[300px]">
      <div class="relative z-10">
        <h1 class="font-headline-h1 text-headline-h1 text-ivory-white mb-4">
          Welcome back,<br /><span class="text-flame-orange">{user?.full_name || "Guest"}!</span>
        </h1>
        <p class="text-body-lg text-muted-gray max-w-md">Your kitchen is warming up. We've curated a few specials based on your love for Umami flavors.</p>
      </div>
    </div>

    {#if lastOrder}
      <div class="bg-surface-card border border-deep-border rounded-[2rem] p-6 group hover:scale-[1.02] transition-transform duration-500">
        <div class="flex justify-between items-start mb-6">
          <span class="font-label-caps text-label-caps text-flame-orange uppercase tracking-widest">Quick Reorder</span>
          <History size={20} class="text-muted-gray" />
        </div>
        <div class="space-y-4">
          <div>
            <h3 class="font-headline-h3 text-headline-h3 text-ivory-white">{lastOrder.order_number}</h3>
            <p class="text-sm text-muted-gray">Last ordered {new Date(lastOrder.created_at).toLocaleDateString()} • ${Number(lastOrder.total_price).toFixed(2)}</p>
          </div>
          <button onclick={() => goto("/dashboard/menu")} class="w-full bg-flame-orange text-white py-4 rounded-xl font-bold orange-glow flex items-center justify-center gap-2 hover:bg-flame-hover transition-colors cursor-pointer">
            <ShoppingCart size={18} />
            Reorder Now
          </button>
        </div>
      </div>
    {:else}
      <div class="bg-surface-card border border-deep-border rounded-[2rem] p-6 flex items-center justify-center min-h-[200px]">
        <p class="text-muted-gray text-sm">No previous orders yet.</p>
      </div>
    {/if}
  </section>

  <!-- Active Orders Track -->
  {#if activeOrder}
    <section>
      <div class="flex items-center gap-4 mb-6">
        <div class="w-1.5 h-6 bg-flame-orange"></div>
        <h2 class="font-headline-h2 text-headline-h2 text-ivory-white">In the Kitchen</h2>
      </div>
      <div class="bg-surface-charcoal border border-deep-border rounded-2xl p-6 flex flex-col md:flex-row items-center gap-8 relative overflow-hidden">
        <div class="w-24 h-24 bg-surface-card rounded-full flex items-center justify-center border-2 border-flame-orange/30 shrink-0">
          <CookingPot size={40} class="text-flame-orange" />
        </div>
        <div class="flex-1 text-center md:text-left">
          <div class="flex items-center justify-center md:justify-start gap-2 mb-1">
            <span class="text-xs font-bold text-flame-orange uppercase tracking-widest">{activeOrder.order_number}</span>
            <span class="w-1 h-1 bg-muted-gray rounded-full"></span>
            <span class="text-xs text-muted-gray">ETA: 15 mins</span>
          </div>
          <h4 class="font-headline-h3 text-headline-h3 text-ivory-white">Chef is preparing your order</h4>
          <div class="mt-4 w-full bg-surface-card h-2 rounded-full overflow-hidden">
            <div class="bg-flame-orange h-full w-[65%] rounded-full shadow-[0_0_10px_#E8640C]"></div>
          </div>
        </div>
        <div class="flex gap-4">
          <button onclick={() => goto("/dashboard/orders")} class="px-6 py-3 border border-deep-border rounded-xl text-sm font-bold text-ivory-white hover:bg-surface-card transition-colors cursor-pointer">Track Live</button>
        </div>
      </div>
    </section>
  {/if}

  <!-- Rewards & Points Bento -->
  <section class="grid grid-cols-1 md:grid-cols-2 gap-8">
    <div class="bg-gradient-to-br from-flame-orange to-[#a04100] rounded-[2rem] p-8 text-white relative overflow-hidden">
      <div class="relative z-10">
        <div class="flex justify-between items-start mb-10">
          <div>
            <p class="font-label-caps text-xs uppercase opacity-80 mb-1">Available Balance</p>
            <h3 class="font-headline-h1 text-4xl font-extrabold tracking-tight">2,450 <span class="text-lg font-medium opacity-70">Points</span></h3>
          </div>
          <div class="w-12 h-12 bg-white/20 rounded-full flex items-center justify-center backdrop-blur-md">
            <Stars size={24} />
          </div>
        </div>
        <div class="space-y-4">
          <div class="flex justify-between text-sm">
            <span>Progress to free Gold Plate</span>
            <span>82%</span>
          </div>
          <div class="w-full bg-black/20 h-3 rounded-full">
            <div class="bg-white h-full w-[82%] rounded-full shadow-lg"></div>
          </div>
          <p class="text-xs opacity-70">Just 550 more points for a complimentary signature appetizer.</p>
        </div>
      </div>
      <div class="absolute -right-10 -bottom-10 w-48 h-48 bg-white/10 rounded-full blur-3xl"></div>
    </div>
    <div class="bg-surface-charcoal border border-deep-border rounded-[2rem] p-8 flex flex-col justify-between">
      <div>
        <h3 class="font-headline-h3 text-headline-h3 text-ivory-white mb-2">Member Exclusive</h3>
        <p class="text-muted-gray text-sm">Access to the Secret Menu: "Truffle Infused Delights" available until midnight.</p>
      </div>
      <div class="mt-6 flex items-center justify-between bg-surface p-4 rounded-xl border border-deep-border border-dashed">
        <div class="flex items-center gap-3">
          <ReceiptText size={20} class="text-flame-orange" />
          <span class="font-label-caps text-xs tracking-widest text-ivory-white">WP-TRUFFLE-25</span>
        </div>
        <button onclick={copyPromoCode} class="text-flame-orange font-bold text-xs uppercase tracking-tighter hover:underline cursor-pointer">Copy Code</button>
      </div>
    </div>
  </section>

  <!-- Quick Order Grid: Most Loved -->
  <section>
    <div class="flex items-center justify-between mb-8">
      <div class="flex items-center gap-4">
        <div class="w-1.5 h-6 bg-flame-orange"></div>
        <h2 class="font-headline-h2 text-headline-h2 text-ivory-white">Most Loved</h2>
      </div>
      <a href="/menu" class="text-flame-orange font-bold text-sm hover:translate-x-1 transition-transform inline-flex items-center gap-1">
        Explore Full Menu <ArrowRight size={14} />
      </a>
    </div>
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
      {#each menuItems.slice(0, 4) as item}
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
          <p class="text-xs text-muted-gray mb-4 line-clamp-1">{item.description || ""}</p>
          <div class="flex items-center justify-between">
            <span class="font-label-price text-label-price text-ivory-white">${Number(item.price).toFixed(2)}</span>
            <button onclick={() => addToCart(item)} class="w-10 h-10 bg-surface-charcoal border border-deep-border rounded-full flex items-center justify-center text-flame-orange hover:bg-flame-orange hover:text-white transition-all duration-300 cursor-pointer">
              <Plus size={18} />
            </button>
          </div>
        </div>
      {:else}
        {#each [1, 2, 3, 4] as _}
          <div class="bg-surface-card rounded-[1.5rem] p-4 border border-deep-border">
            <div class="rounded-xl overflow-hidden aspect-square mb-4 bg-surface-charcoal flex items-center justify-center">
              <p class="text-muted-gray text-xs">No items yet</p>
            </div>
          </div>
        {/each}
      {/each}
    </div>
  </section>

  <!-- Recent Activity -->
  <section class="pb-section-gap">
    <div class="bg-surface-charcoal border border-deep-border rounded-[2rem] overflow-hidden">
      <div class="p-8 border-b border-deep-border flex items-center justify-between">
        <h3 class="font-headline-h3 text-headline-h3 text-ivory-white">Recent Culinary Journeys</h3>
        <button onclick={() => goto("/dashboard/orders")} class="text-sm text-muted-gray hover:text-flame-orange transition-colors cursor-pointer">Download History</button>
      </div>
      <div class="divide-y divide-deep-border">
        {#each recentOrders as order}
          <a href="/dashboard/orders/{order.id}" class="p-6 flex items-center justify-between hover:bg-surface-card transition-colors block">
            <div class="flex items-center gap-4">
              <div class="w-12 h-12 rounded-xl bg-surface flex items-center justify-center">
                <span class="text-muted-gray font-bold text-lg">#</span>
              </div>
              <div>
                <p class="font-bold text-ivory-white">{order.order_number}</p>
                <p class="text-xs text-muted-gray">{new Date(order.created_at).toLocaleDateString()} • {order.items?.length || 0} Items</p>
              </div>
            </div>
            <div class="text-right">
              <p class="font-label-price text-sm text-ivory-white">${Number(order.total_price).toFixed(2)}</p>
              <p class={"text-[10px] font-bold uppercase tracking-widest " + statusColor(order.status)}>{order.status}</p>
            </div>
          </a>
        {:else}
          <div class="p-12 text-center">
            <p class="text-muted-gray">No culinary journeys yet. Start exploring our menu!</p>
            <a href="/menu" class="inline-block mt-4 bg-flame-orange hover:bg-flame-hover text-white px-8 py-3 rounded-full font-bold text-sm transition-all">
              Browse Menu
            </a>
          </div>
        {/each}
      </div>
      {#if recentOrders.length > 0}
        <div class="p-6 text-center">
          <a href="/account/orders" class="text-muted-gray text-xs font-bold uppercase tracking-widest hover:text-flame-orange transition-colors">View All Activity</a>
        </div>
      {/if}
    </div>
  </section>
{/if}
