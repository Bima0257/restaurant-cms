<script lang="ts">
  import { onMount } from "svelte";
  import { goto } from "$app/navigation";
  import { get } from "svelte/store";
  import { auth } from "$lib/stores/auth";
  import "../layout.css";
  import StaffSidebar from "$lib/components/staff/StaffSidebar.svelte";
  import AdminHeader from "$lib/components/admin/AdminHeader.svelte";

  let { children } = $props();
  let authed = $state(false);

  onMount(() => {
    const user = get(auth);
    if (!user || user.role !== "staff") {
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
  <StaffSidebar />
  <div class="flex-1 flex flex-col">
    <AdminHeader />
    <main class="flex-1 p-6">
      {@render children()}
    </main>
  </div>
</div>
