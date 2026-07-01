<script lang="ts">
  import { onMount } from "svelte";
  import { goto } from "$app/navigation";
  import { get } from "svelte/store";
  import { auth } from "$lib/stores/auth";
  import Sidebar from "$lib/components/admin/Sidebar.svelte";
  import AdminHeader from "$lib/components/admin/AdminHeader.svelte";

  let { children } = $props();
  let authed = $state(false);

  onMount(() => {
    const user = get(auth);
    if (!user || user.role !== "admin") {
      goto(user ? "/dashboard" : "/auth/login");
      return;
    }
    authed = true;
  });
</script>

{#if authed}
{@render children()}
{/if}

<div class="flex min-h-screen bg-surface">
  <Sidebar />
  <div class="flex-1 flex flex-col">
    <AdminHeader />
    <main class="flex-1 p-6">
      {@render children()}
    </main>
  </div>
</div>
