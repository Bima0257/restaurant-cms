<script lang="ts">
  import { page } from "$app/stores";
  import { goto } from "$app/navigation";
  import {
    Shield,
    Users,
    ClipboardList,
    Database,
    Settings,
    LogOut,
  } from "@lucide/svelte";
  import { toast } from "svelte-sonner";
  import { auth } from "$lib/stores/auth";
  import { api } from "$lib/api";

  interface NavItem {
    label: string;
    href: string;
    icon: typeof Shield;
  }

  interface NavSection {
    label: string;
    items: NavItem[];
  }

  const sections: NavSection[] = [
    {
      label: "Users",
      items: [
        { label: "Admins", href: "/superadmin/admins", icon: Shield },
        { label: "Staff", href: "/superadmin/staff", icon: Users },
      ],
    },
    {
      label: "System",
      items: [
        { label: "Audit Log", href: "/superadmin/audit-log", icon: ClipboardList },
        { label: "Database", href: "/superadmin/backup", icon: Database },
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
    <a href="/superadmin/admins" class="font-headline-h3 text-headline-h3 text-flame-orange font-extrabold">WorldPlate</a>
    <p class="text-muted-gray text-xs mt-1">Superadmin Panel</p>
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
                class={$page.url.pathname.startsWith(item.href)
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

  <div class="p-4 border-t border-deep-border space-y-1">
    <a
      href="/admin"
      class="flex items-center gap-3 px-3 py-2.5 rounded-xl text-muted-gray hover:text-ivory-white hover:bg-surface-charcoal transition-colors"
    >
      <Settings size={18} />
      <span class="text-sm">Admin Dashboard</span>
    </a>
    <button
      onclick={handleLogout}
      class="flex items-center gap-3 px-3 py-2.5 rounded-xl text-muted-gray hover:text-red-400 hover:bg-red-500/10 transition-colors w-full cursor-pointer"
    >
      <LogOut size={18} />
      <span class="text-sm">Logout</span>
    </button>
  </div>
</aside>
