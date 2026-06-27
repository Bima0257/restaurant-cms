<script lang="ts">
  import { onMount } from "svelte";
  import { Database, Download, Upload, Trash2, RotateCcw, Loader2, AlertTriangle } from "@lucide/svelte";
  import { toast } from "svelte-sonner";
  import { confirmAction } from "$lib/utils/confirm";
  import { api } from "$lib/api";

  let backups = $state<{ filename: string; size: number; created_at: string }[]>([]);
  let loading = $state(false);
  let creating = $state(false);
  let restoring = $state(false);

  let showRestoreModal = $state(false);
  let restoreFile = $state<File | null>(null);

  function formatSize(bytes: number): string {
    if (bytes < 1024) return bytes + " B";
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + " KB";
    return (bytes / (1024 * 1024)).toFixed(1) + " MB";
  }

  function formatDate(iso: string): string {
    const d = new Date(iso);
    return d.toLocaleDateString("id-ID", { year: "numeric", month: "short", day: "numeric", hour: "2-digit", minute: "2-digit" });
  }

  async function loadBackups() {
    try {
      backups = await api.superadminListBackups();
    } catch (err: any) {
      toast.error(err.message);
    }
  }

  async function handleCreate() {
    creating = true;
    try {
      const res = await api.superadminCreateBackup();
      toast.success(`Backup created: ${res.filename}`);
      await loadBackups();
    } catch (err: any) {
      toast.error(err.message);
    } finally {
      creating = false;
    }
  }

  async function handleDownload(filename: string) {
    try {
      await api.superadminDownloadBackup(filename);
    } catch (err: any) {
      toast.error(err.message);
    }
  }

  async function handleDelete(filename: string) {
    const confirmed = await confirmAction({
      title: "Delete Backup",
      message: `Are you sure you want to delete "${filename}"? This action cannot be undone.`,
      confirmLabel: "Delete",
      variant: "danger",
    });
    if (!confirmed) return;
    try {
      await api.superadminDeleteBackup(filename);
      toast.success("Backup deleted");
      await loadBackups();
    } catch (err: any) {
      toast.error(err.message);
    }
  }

  function openRestoreModal() {
    showRestoreModal = true;
    restoreFile = null;
  }

  async function confirmRestore() {
    if (!restoreFile) return;
    restoring = true;
    try {
      const res = await api.superadminRestoreBackup(restoreFile);
      toast.success(res.message);
      showRestoreModal = false;
    } catch (err: any) {
      toast.error(err.message);
    } finally {
      restoring = false;
    }
  }

  onMount(loadBackups);
</script>

<div class="p-6 max-w-4xl mx-auto">
  <div class="mb-6 flex items-center justify-between">
    <div>
      <h1 class="font-headline-h3 text-headline-h3 text-ivory-white">Database</h1>
      <p class="text-muted-gray text-sm mt-1">Backup & restore database</p>
    </div>
    <div class="flex gap-3">
      <button
        onclick={handleCreate}
        disabled={creating}
        class="bg-flame-orange hover:bg-flame-hover text-ivory-white px-5 py-2.5 rounded-full font-bold text-sm transition-all flex items-center gap-2 disabled:opacity-50 cursor-pointer"
      >
        {#if creating}
          <Loader2 size={16} class="animate-spin" />
          Creating...
        {:else}
          <Database size={16} />
          Create Backup
        {/if}
      </button>
      <button
        onclick={openRestoreModal}
        class="bg-surface-charcoal hover:bg-deep-border text-ivory-white px-5 py-2.5 rounded-full font-bold text-sm transition-all flex items-center gap-2 cursor-pointer"
      >
        <RotateCcw size={16} />
        Restore
      </button>
    </div>
  </div>

  <div class="bg-surface-card rounded-2xl border border-deep-border overflow-hidden">
    <div class="px-5 py-3 border-b border-deep-border">
      <h2 class="text-ivory-white font-bold text-sm">Backup Files</h2>
    </div>
    {#if backups.length === 0}
      <div class="p-8 text-center text-muted-gray text-sm">No backup files yet.</div>
    {:else}
      <div class="divide-y divide-deep-border">
        {#each backups as bf}
          <div class="flex items-center justify-between px-5 py-3">
            <div class="min-w-0 flex-1">
              <p class="text-ivory-white text-sm truncate">{bf.filename}</p>
              <p class="text-muted-gray text-xs mt-0.5">{formatSize(bf.size)} &middot; {formatDate(bf.created_at)}</p>
            </div>
            <div class="flex items-center gap-2 shrink-0 ml-4">
              <button onclick={() => handleDownload(bf.filename)} class="text-muted-gray hover:text-flame-orange transition-colors p-1.5 cursor-pointer" title="Download">
                <Download size={16} />
              </button>
              <button onclick={() => handleDelete(bf.filename)} class="text-muted-gray hover:text-red-400 transition-colors p-1.5 cursor-pointer" title="Delete">
                <Trash2 size={16} />
              </button>
            </div>
          </div>
        {/each}
      </div>
    {/if}
  </div>
</div>

{#if showRestoreModal}
  <div class="fixed inset-0 bg-black/60 flex items-center justify-center z-50 p-4" onclick={() => showRestoreModal = false}>
    <div class="bg-surface-card rounded-3xl p-6 w-full max-w-md" onclick={(e) => e.stopPropagation()}>
      <div class="text-center mb-4">
        <div class="flex justify-center mb-3">
          <div class="bg-red-500/10 p-3 rounded-full">
            <AlertTriangle size={28} class="text-red-400" />
          </div>
        </div>
        <h2 class="text-ivory-white font-bold text-lg">Restore Database</h2>
        <p class="text-muted-gray text-sm mt-1">
          This will <span class="text-red-400 font-semibold">overwrite all existing data</span>. This action cannot be undone.
        </p>
      </div>

      <div class="mb-4">
        <label class="block text-sm text-muted-gray mb-1">Upload .sql backup file</label>
        <input
          type="file"
          accept=".sql"
          onchange={(e) => { const input = e.currentTarget as HTMLInputElement; restoreFile = input.files?.[0] || null; }}
          class="block w-full text-sm text-muted-gray file:mr-3 file:py-2 file:px-4 file:rounded-xl file:border-0 file:text-sm file:font-bold file:bg-flame-orange file:text-ivory-white hover:file:bg-flame-hover cursor-pointer"
        />
      </div>

      <div class="flex gap-3">
        <button
          onclick={() => showRestoreModal = false}
          class="flex-1 bg-surface-charcoal hover:bg-deep-border text-ivory-white py-2.5 rounded-full font-bold text-sm transition-all cursor-pointer"
        >
          Cancel
        </button>
        <button
          onclick={confirmRestore}
          disabled={!restoreFile || restoring}
          class="flex-1 bg-red-500 hover:bg-red-600 text-white py-2.5 rounded-full font-bold text-sm transition-all flex items-center justify-center gap-2 disabled:opacity-50 cursor-pointer"
        >
          {#if restoring}
            <Loader2 size={16} class="animate-spin" />
            Restoring...
          {:else}
            <Upload size={16} />
            Restore
          {/if}
        </button>
      </div>
    </div>
  </div>
{/if}
