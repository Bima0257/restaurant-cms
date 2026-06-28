<script lang="ts">
  import "../layout.css";
  import { LayoutDashboard, ShoppingBag, Award, User } from "@lucide/svelte";
  import CustomerSidebar from "$lib/components/customer/CustomerSidebar.svelte";
  import CustomerHeader from "$lib/components/customer/CustomerHeader.svelte";
  import MobileBottomNav from "$lib/components/ui/MobileBottomNav.svelte";

  let { children } = $props();

  const mobileTabs = [
    { label: "Dashboard", href: "/dashboard", icon: LayoutDashboard },
    { label: "Orders", href: "/account/orders", icon: ShoppingBag },
    { label: "Rewards", href: "#", icon: Award },
    { label: "Profile", href: "#", icon: User },
  ];
</script>

<div class="flex min-h-screen overflow-hidden bg-surface">
  <CustomerSidebar />

  <main class="flex-1 relative h-screen overflow-y-auto bg-surface custom-scrollbar">
    <CustomerHeader />

    <div class="px-gutter py-8 space-y-10 max-w-grid-max-width mx-auto">
      {@render children()}
    </div>

    <MobileBottomNav items={mobileTabs} />
  </main>
</div>

<style>
  .custom-scrollbar::-webkit-scrollbar { width: 4px; }
  .custom-scrollbar::-webkit-scrollbar-track { background: #131313; }
  .custom-scrollbar::-webkit-scrollbar-thumb { background: #2E2E2E; border-radius: 10px; }
</style>
