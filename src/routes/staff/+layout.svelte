<script lang="ts">
  import "../layout.css";
  import StaffSidebar from "$lib/components/staff/StaffSidebar.svelte";
  import AdminHeader from "$lib/components/admin/AdminHeader.svelte";

  let { children } = $props();
</script>

<div class="flex min-h-screen bg-surface">
  <StaffSidebar />
  <div class="flex-1 flex flex-col">
    <AdminHeader />
    <main class="flex-1 p-6">
      {@render children()}
    </main>
  </div>
</div>
