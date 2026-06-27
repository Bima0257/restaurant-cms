<script lang="ts">
  import { Search, Bell } from "@lucide/svelte";
  import { auth } from "$lib/stores/auth";
  import { get } from "svelte/store";

  let user = $derived(get(auth));
</script>

<header class="sticky top-0 z-40 bg-surface/80 backdrop-blur-md px-gutter py-6 flex items-center justify-between">
  <div class="flex-1 max-w-xl">
    <div class="relative group">
      <Search
        size={20}
        class="absolute left-4 top-1/2 -translate-y-1/2 text-muted-gray group-focus-within:text-flame-orange transition-colors"
      />
      <input
        class="w-full bg-surface-charcoal border border-deep-border rounded-full py-3 pl-12 pr-6 text-ivory-white focus:outline-none focus:border-flame-orange focus:ring-1 focus:ring-flame-orange transition-all duration-300"
        placeholder="Search for your next craving..."
        type="text"
      />
    </div>
  </div>
  <div class="flex items-center gap-6 ml-8">
    <button class="relative text-muted-gray hover:text-flame-orange transition-colors cursor-pointer">
      <Bell size={22} />
      <span class="absolute top-0 right-0 w-2 h-2 bg-flame-orange rounded-full border-2 border-surface"></span>
    </button>
    <div class="flex items-center gap-3">
      <div class="text-right hidden sm:block">
        <p class="font-bold text-sm text-ivory-white">{user?.full_name || "Guest"}</p>
        <p class="text-xs text-flame-orange">Elite Member</p>
      </div>
      <div class="w-12 h-12 rounded-full border-2 border-flame-orange p-0.5">
        {#if user?.avatar_url}
          <img class="w-full h-full rounded-full object-cover" alt={user.full_name} src={user.avatar_url} />
        {:else}
          <div class="w-full h-full rounded-full bg-flame-orange/20 flex items-center justify-center text-flame-orange font-bold text-sm">
            {user?.full_name?.charAt(0)?.toUpperCase() || "G"}
          </div>
        {/if}
      </div>
    </div>
  </div>
</header>
