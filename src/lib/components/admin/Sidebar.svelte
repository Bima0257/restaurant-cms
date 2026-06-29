<script lang="ts">
  import { page } from "$app/stores";
  import { goto } from "$app/navigation";
  import {
    LayoutDashboard,
    UtensilsCrossed,
    ShoppingCart,
    FolderTree,
    FileText,
    Settings,
    User,
    LogOut,
  } from "@lucide/svelte";
  import { toast } from "svelte-sonner";
  import { auth } from "$lib/stores/auth";
  import { api } from "$lib/api";

  interface NavItem {
    label: string;
    href: string;
    icon: typeof LayoutDashboard;
  }

  interface NavSection {
    label: string;
    items: NavItem[];
  }

  const sections: NavSection[] = [
    {
      label: "Menu",
      items: [
        { label: "Dashboard", href: "/admin", icon: LayoutDashboard },
        { label: "Menu Items", href: "/admin/menu", icon: UtensilsCrossed },
        { label: "Categories", href: "/admin/categories", icon: FolderTree },
      ],
    },
    {
      label: "Operations",
      items: [
        { label: "Orders", href: "/admin/orders", icon: ShoppingCart },
        { label: "Reports", href: "/admin/reports", icon: FileText },
      ],
    },
    {
      label: "System",
      items: [
        { label: "Settings", href: "/admin/settings", icon: Settings },
        { label: "Profile", href: "/admin/profile", icon: User },
      ],
    },
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

<aside class="w-64 bg-surface-card border-r border-deep-border flex flex-col h-screen sticky top-0">
  <div class="p-6 border-b border-deep-border">
    <a href="/admin" class="font-headline-h3 text-headline-h3 text-flame-orange font-extrabold">WorldPlate</a>
    <p class="text-muted-gray text-xs mt-1">Admin Panel</p>
  </div>

  <nav class="flex-1 p-4 overflow-y-auto">
    {#each sections as section}
      <div class="mb-4">
        <p class="text-muted-gray text-[10px] font-semibold uppercase tracking-wider px-3 mb-1">{section.label}</p>
        <ul class="flex flex-col gap-0.5">
          {#each section.items as item}
            <li>
              <a
                href={item.href}
                class={$page.url.pathname === item.href || (item.href !== "/admin" && $page.url.pathname.startsWith(item.href))
                  ? "flex items-center gap-3 px-3 py-2.5 rounded-xl bg-flame-orange/10 text-flame-orange font-medium transition-colors"
                  : "flex items-center gap-3 px-3 py-2.5 rounded-xl text-muted-gray hover:text-ivory-white hover:bg-surface-charcoal transition-colors"}
              >
                <item.icon size={18} />
                <span class="text-sm">{item.label}</span>
              </a>
            </li>
          {/each}
        </ul>
      </div>
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
</aside>
