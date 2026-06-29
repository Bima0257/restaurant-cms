<script lang="ts">
  import { page } from "$app/stores";
  import { goto } from "$app/navigation";
  import { LayoutDashboard, UtensilsCrossed, ShoppingCart, ShoppingBag, Award, User, Headset, LogOut } from "@lucide/svelte";
  import { toast } from "svelte-sonner";
  import { auth } from "$lib/stores/auth";
  import { api } from "$lib/api";

  const navItems = [
    { label: "Dashboard", href: "/dashboard", icon: LayoutDashboard },
    { label: "Menu", href: "/dashboard/menu", icon: UtensilsCrossed },
    { label: "My Orders", href: "/dashboard/orders", icon: ShoppingBag },
    { label: "Cart", href: "/dashboard/cart", icon: ShoppingCart },
    { label: "Rewards", href: "#", icon: Award },
    { label: "Profile", href: "/dashboard/profile", icon: User },
  ];

  async function handleLogout() {
    try {
      const refreshToken = auth.getRefreshToken();
      if (refreshToken) {
        await api.logout(refreshToken);
      }
    } catch { /* ignore */ }
    auth.logout();
    toast.success("Logged out successfully");
    goto("/");
  }
</script>

<aside class="w-72 bg-surface-container-lowest border-r border-deep-border hidden md:flex flex-col z-50 shrink-0 h-screen sticky top-0">
  <div class="p-8">
    <a href="/" class="font-headline-h3 text-headline-h3 font-extrabold text-flame-orange">WorldPlate</a>
  </div>
  <nav class="flex-1 px-4 space-y-2 mt-4">
    {#each navItems as item}
      <a
        href={item.href}
        class={$page.url.pathname === item.href
          ? "flex items-center gap-3 px-4 py-3 bg-flame-orange text-white rounded-xl font-bold transition-all duration-300"
          : "flex items-center gap-3 px-4 py-3 text-muted-gray hover:text-flame-orange transition-colors duration-300"}
      >
        <item.icon size={20} />
        <span>{item.label}</span>
      </a>
    {/each}
  </nav>
  <div class="p-4 border-t border-deep-border">
    <button
      onclick={handleLogout}
      class="flex items-center gap-3 px-3 py-2.5 rounded-xl text-muted-gray hover:text-red-400 hover:bg-red-500/10 transition-colors w-full cursor-pointer"
    >
      <LogOut size={18} />
      <span class="text-sm">Logout</span>
    </button>
  </div>
  <div class="p-6">
    <div class="bg-surface-card p-4 rounded-2xl border border-deep-border">
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 rounded-full bg-flame-orange/20 flex items-center justify-center">
          <Headset size={20} class="text-flame-orange" />
        </div>
        <div>
          <p class="text-sm font-bold text-ivory-white">Need help?</p>
          <p class="text-xs text-muted-gray">24/7 Concierge</p>
        </div>
      </div>
    </div>
  </div>
</aside>
