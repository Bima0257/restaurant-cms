<script lang="ts">
  import { Search, LogOut, User } from "@lucide/svelte";
  import { goto } from "$app/navigation";
  import { toast } from "svelte-sonner";
  import { auth } from "$lib/stores/auth";
  import { api } from "$lib/api";

  const user = $derived($auth);

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

<header class="h-16 bg-surface-card border-b border-deep-border flex items-center justify-between px-6 sticky top-0 z-30">
  <div class="flex items-center gap-4 flex-1 max-w-md">
    <div class="relative w-full">
      <Search size={16} class="absolute left-3 top-1/2 -translate-y-1/2 text-muted-gray" />
      <input
        class="w-full bg-surface-charcoal border border-deep-border rounded-xl pl-10 pr-4 py-2 text-sm focus:border-flame-orange focus:ring-0 outline-none text-ivory-white"
        placeholder="Search..."
        type="text"
      />
    </div>
  </div>

  <div class="flex items-center gap-4">
    <div class="flex items-center gap-3">
      <div class="text-right">
        <p class="text-sm font-medium text-ivory-white">{user?.full_name || "User"}</p>
        <p class="text-xs text-muted-gray">{user?.email || ""}</p>
      </div>
      {#if user?.avatar_url}
        <img
          class="w-9 h-9 rounded-full border-2 border-flame-orange object-cover"
          alt="User avatar"
          src={user.avatar_url}
        />
      {:else}
        <div class="w-9 h-9 rounded-full border-2 border-flame-orange bg-surface-charcoal flex items-center justify-center">
          <User size={16} class="text-muted-gray" />
        </div>
      {/if}
    </div>
    <button
      onclick={handleLogout}
      class="flex items-center gap-2 px-3 py-2 rounded-xl text-muted-gray hover:text-red-400 hover:bg-red-500/10 transition-colors cursor-pointer"
    >
      <LogOut size={18} />
      <span class="text-sm font-medium">Logout</span>
    </button>
  </div>
</header>
