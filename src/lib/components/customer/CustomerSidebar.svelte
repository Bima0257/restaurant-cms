<script lang="ts">
  import { page } from "$app/stores";
  import { LayoutDashboard, ShoppingBag, Heart, Award, Settings, Headset } from "@lucide/svelte";

  const navItems = [
    { label: "Dashboard", href: "/dashboard", icon: LayoutDashboard },
    { label: "My Orders", href: "/account/orders", icon: ShoppingBag },
    { label: "Favorite Dishes", href: "#", icon: Heart },
    { label: "Rewards", href: "#", icon: Award },
    { label: "Settings", href: "#", icon: Settings },
  ];
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
  <div class="p-6 mt-auto">
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
