<script lang="ts">
  import { onMount } from "svelte";
  import { ClipboardList } from "@lucide/svelte";
  import { toast } from "svelte-sonner";
  import { api } from "$lib/api";
  import DataTable from "$lib/components/ui/DataTable.svelte";

  let logs = $state<any[]>([]);
  let loading = $state(true);

  const columns = [
    { key: "created_at", label: "Time" },
    { key: "email", label: "Email" },
    { key: "user_role", label: "Role" },
    { key: "activity", label: "Activity" },
    { key: "module", label: "Module" },
    { key: "description", label: "Description" },
    { key: "ip_address", label: "IP" },
  ];

   onMount(async () => {
      try {
        logs = await api.superadminGetAuditLog();
      } catch (err: any) {
        toast.error(err.message || "Failed to load audit log");
      } finally {
        loading = false;
      }
    });

  function activityBadge(activity: string): string {
    if (activity.includes("Login") || activity.includes("Logout") || activity.includes("Register")) return "bg-blue-500/10 text-blue-400";
    if (activity.includes("Create") || activity.includes("Stock In")) return "bg-green-500/10 text-green-400";
    if (activity.includes("Update") || activity.includes("Change") || activity.includes("Reset")) return "bg-yellow-500/10 text-yellow-400";
    if (activity.includes("Delete") || activity.includes("Restore")) return "bg-red-500/10 text-red-400";
    if (activity.includes("Backup")) return "bg-purple-500/10 text-purple-400";
    return "bg-gray-500/10 text-gray-400";
  }
</script>

<div class="mb-8">
  <h1 class="font-headline-h2 text-headline-h2 text-ivory-white">Audit Log</h1>
  <p class="text-muted-gray text-sm mt-1">Track all system activities</p>
</div>

<div class="bg-surface-card rounded-2xl border border-deep-border p-6">
  {#if loading}
    <p class="text-muted-gray">Loading...</p>
  {:else if logs.length === 0}
    <div class="text-center py-12">
      <ClipboardList size={48} class="text-muted-gray mx-auto mb-3" />
      <p class="text-muted-gray">No audit logs yet</p>
    </div>
  {:else}
    <DataTable {columns} rows={logs}>
      {#snippet cell({ col, row })}
        {#if col.key === "created_at"}
          <span class="text-muted-gray text-xs whitespace-nowrap">{new Date(row.created_at).toLocaleString("id-ID")}</span>
        {:else if col.key === "user_role"}
          <span class="text-xs px-2 py-0.5 rounded-full bg-surface-charcoal text-muted-gray capitalize">{row.user_role}</span>
        {:else if col.key === "activity"}
          <span class="text-xs px-2 py-1 rounded-full font-medium {activityBadge(row.activity)}">{row.activity}</span>
        {:else if col.key === "description"}
          <span class="text-ivory-white max-w-xs truncate block">{row.description || "-"}</span>
        {:else if col.key === "ip_address"}
          <span class="text-muted-gray text-xs">{row.ip_address || "-"}</span>
        {:else if col.key === "email"}
          <span class="text-ivory-white font-medium">{row.email}</span>
        {:else}
          <span class="text-muted-gray">{row[col.key] || "-"}</span>
        {/if}
      {/snippet}
    </DataTable>
  {/if}
</div>
