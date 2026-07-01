<script lang="ts">
  import { onMount } from "svelte";
  import { goto } from "$app/navigation";
  import { Loader2 } from "@lucide/svelte";
  import { toast } from "svelte-sonner";
  import { api } from "$lib/api";
  import { auth } from "$lib/stores/auth";
  import { get } from "svelte/store";
  import StatCard from "$lib/components/admin/StatCard.svelte";
  import {
    UtensilsCrossed,
    ShoppingCart,
    DollarSign,
    Users,
  } from "@lucide/svelte";
  import SectionHeading from "$lib/components/ui/SectionHeading.svelte";

  let loading = $state(true);
  let menuItems: any[] = $state([]);
  let orders: any[] = $state([]);

  onMount(async () => {
    if (!get(auth)) {
      goto("/auth/login");
      return;
    }
    try {
      const [menuRes, ordersRes] = await Promise.all([
        api.adminListMenu().catch(() => []),
        api.adminListOrders().catch(() => []),
      ]);
      menuItems = menuRes;
      orders = ordersRes;
    } catch { /* ignore */ }
    loading = false;
  });

  let stats = $derived([
    { title: "Total Menu Items", value: String(menuItems.length), icon: UtensilsCrossed, trend: `${menuItems.length}`, trendUp: true },
    { title: "Total Orders", value: String(orders.length), icon: ShoppingCart, trend: `${orders.filter((o) => o.status === "pending").length} pending`, trendUp: true },
    { title: "Revenue", value: `$${orders.reduce((sum, o) => sum + Number(o.total_price), 0).toFixed(0)}`, icon: DollarSign, trend: `${orders.filter((o) => o.payment_status === "paid").length} paid`, trendUp: true },
    { title: "Active Items", value: String(menuItems.filter((m) => m.is_available).length), icon: Users, trend: `${menuItems.filter((m) => !m.is_available).length} unavailable`, trendUp: false },
  ]);

  const statusColors: Record<string, string> = {
    pending: "text-yellow-400",
    confirmed: "text-blue-400",
    preparing: "text-flame-orange",
    ready: "text-purple-400",
    delivered: "text-green-400",
    completed: "text-green-400",
    cancelled: "text-red-400",
  };

  const statusBg: Record<string, string> = {
    pending: "bg-yellow-500/10 border-yellow-500/20",
    confirmed: "bg-blue-500/10 border-blue-500/20",
    preparing: "bg-flame-orange/10 border-flame-orange/20",
    ready: "bg-purple-500/10 border-purple-500/20",
    delivered: "bg-green-500/10 border-green-500/20",
    completed: "bg-green-500/10 border-green-500/20",
    cancelled: "bg-red-500/10 border-red-500/20",
  };

  function label(str: string) {
    return str.charAt(0).toUpperCase() + str.slice(1);
  }

  function formatPrice(price: number) {
    return `$${Number(price).toFixed(2)}`;
  }

  function formatDate(dateStr: string) {
    const d = new Date(dateStr);
    return d.toLocaleDateString("en-US", { month: "short", day: "numeric", hour: "2-digit", minute: "2-digit" });
  }

  let recentOrders = $derived(orders.slice(0, 5));
</script>

<div class="mb-8">
  <SectionHeading prefix="Admin" highlight="Dashboard" />
</div>

{#if loading}
  <div class="flex items-center justify-center py-12">
    <Loader2 size={24} class="animate-spin text-muted-gray" />
  </div>
{:else}
  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
    {#each stats as stat}
      <StatCard {...stat} />
    {/each}
  </div>

  <div class="bg-surface-card rounded-2xl border border-deep-border p-6">
    <div class="flex items-center justify-between mb-6">
      <h3 class="font-headline-h3 text-headline-h3 text-ivory-white">Recent Orders</h3>
      <a href="/admin/orders" class="text-sm text-flame-orange hover:underline">View All</a>
    </div>
    {#if recentOrders.length === 0}
      <p class="text-muted-gray text-sm text-center py-8">No orders yet</p>
    {:else}
      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead>
            <tr class="border-b border-deep-border">
              <th class="text-left py-3 px-4 text-muted-gray font-medium text-[10px] uppercase tracking-wider">Order</th>
              <th class="text-left py-3 px-4 text-muted-gray font-medium text-[10px] uppercase tracking-wider hidden md:table-cell">Date</th>
              <th class="text-left py-3 px-4 text-muted-gray font-medium text-[10px] uppercase tracking-wider">Total</th>
              <th class="text-left py-3 px-4 text-muted-gray font-medium text-[10px] uppercase tracking-wider">Status</th>
            </tr>
          </thead>
          <tbody>
            {#each recentOrders as order}
              <tr class="border-b border-deep-border/50 hover:bg-surface-charcoal/40 transition-colors">
                <td class="py-3 px-4 text-ivory-white font-medium">{order.order_number}</td>
                <td class="py-3 px-4 text-muted-gray text-sm hidden md:table-cell">{formatDate(order.created_at)}</td>
                <td class="py-3 px-4 text-ivory-white">{formatPrice(order.total_price)}</td>
                <td class="py-3 px-4">
                  <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border {statusBg[order.status] || 'bg-gray-500/10 border-gray-500/20'} {statusColors[order.status] || 'text-muted-gray'}">
                    {label(order.status)}
                  </span>
                </td>
              </tr>
            {/each}
          </tbody>
        </table>
      </div>
    {/if}
  </div>
{/if}
