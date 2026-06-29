<script lang="ts">
  import { FileText, Download, Loader2, Calendar, X, Eye } from "@lucide/svelte";
  import { toast } from "svelte-sonner";
  import { api } from "$lib/api";

  const reportTypes = [
    { id: "sales", label: "Sales Report", desc: "Daily revenue and order count" },
    { id: "orders", label: "Orders Report", desc: "All orders with status and payment" },
    { id: "stock", label: "Stock Report", desc: "Current ingredient stock levels" },
    { id: "ingredient-usage", label: "Ingredient Usage", desc: "Ingredient consumption history" },
    { id: "best-menu", label: "Best Menu Items", desc: "Top selling menu items by quantity" },
    { id: "activities", label: "Activity Report", desc: "User activities and stock changes" },
  ];

  let startDate = $state("");
  let endDate = $state("");
  let loading = $state<string | null>(null);
  let previewBlobUrl = $state<string | null>(null);
  let previewLabel = $state("");

  async function handlePreview(reportType: string) {
    loading = reportType;
    try {
      const params: Record<string, string> = {};
      if (startDate) params.start_date = startDate;
      if (endDate) params.end_date = endDate;
      const blob = await api.fetchReportBlob(reportType, params);
      if (previewBlobUrl) URL.revokeObjectURL(previewBlobUrl);
      previewBlobUrl = URL.createObjectURL(blob);
      previewLabel = reportTypes.find((r) => r.id === reportType)?.label || reportType;
    } catch (err: any) {
      toast.error(err.message);
    } finally {
      loading = null;
    }
  }

  function handleDownload() {
    if (!previewBlobUrl) return;
    const a = document.createElement("a");
    a.href = previewBlobUrl;
    a.download = `${previewLabel.toLowerCase().replace(/\s+/g, "_")}_report.pdf`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  }

  function closePreview() {
    if (previewBlobUrl) URL.revokeObjectURL(previewBlobUrl);
    previewBlobUrl = null;
    previewLabel = "";
  }
</script>

<div class="p-6 max-w-4xl mx-auto">
  <div class="mb-6">
    <h1 class="font-headline-h3 text-headline-h3 text-ivory-white">Reports</h1>
    <p class="text-muted-gray text-sm mt-1">Generate and preview PDF reports</p>
  </div>

  <div class="bg-surface-card rounded-2xl p-4 mb-6 flex flex-wrap gap-4 items-end">
    <div>
      <label class="text-xs text-muted-gray block mb-1">Start Date</label>
      <div class="relative">
        <Calendar size={14} class="absolute left-3 top-1/2 -translate-y-1/2 text-muted-gray" />
        <input
          type="date"
          bind:value={startDate}
          class="bg-surface-charcoal border border-deep-border rounded-xl pl-9 pr-3 py-2 text-sm text-ivory-white focus:border-flame-orange outline-none"
        />
      </div>
    </div>
    <div>
      <label class="text-xs text-muted-gray block mb-1">End Date</label>
      <div class="relative">
        <Calendar size={14} class="absolute left-3 top-1/2 -translate-y-1/2 text-muted-gray" />
        <input
          type="date"
          bind:value={endDate}
          class="bg-surface-charcoal border border-deep-border rounded-xl pl-9 pr-3 py-2 text-sm text-ivory-white focus:border-flame-orange outline-none"
        />
      </div>
    </div>
    <button
      onclick={() => { startDate = ""; endDate = ""; }}
      class="text-xs text-muted-gray hover:text-ivory-white transition-colors cursor-pointer"
    >
      Clear dates
    </button>
  </div>

  <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
    {#each reportTypes as report}
      <div class="bg-surface-card rounded-2xl p-5 border border-deep-border">
        <div class="flex items-start gap-3">
          <div class="bg-flame-orange/10 p-3 rounded-xl shrink-0">
            <FileText size={20} class="text-flame-orange" />
          </div>
          <div class="flex-1 min-w-0">
            <h3 class="text-ivory-white font-bold text-sm">{report.label}</h3>
            <p class="text-muted-gray text-xs mt-1">{report.desc}</p>
          </div>
          <button
            onclick={() => handlePreview(report.id)}
            disabled={loading !== null}
            class="bg-flame-orange hover:bg-flame-hover text-ivory-white p-2.5 rounded-xl transition-all disabled:opacity-50 cursor-pointer shrink-0"
            title="Preview"
          >
            {#if loading === report.id}
              <Loader2 size={16} class="animate-spin" />
            {:else}
              <Eye size={16} />
            {/if}
          </button>
        </div>
      </div>
    {/each}
  </div>
</div>

{#if previewBlobUrl}
  <div
    class="fixed inset-0 bg-black/70 flex items-center justify-center z-50"
    onclick={() => closePreview()}
    onkeydown={(e) => { if (e.key === "Escape") closePreview(); }}
    role="dialog"
    tabindex={-1}
  >
    <div
      class="bg-surface-card w-full h-full flex flex-col border border-deep-border overflow-hidden"
      onclick={(e) => e.stopPropagation()}
    >
      <div class="flex items-center justify-between px-6 py-4 border-b border-deep-border shrink-0">
        <h3 class="font-headline-h3 text-headline-h3 text-ivory-white">{previewLabel}</h3>
        <div class="flex items-center gap-3">
          <button
            onclick={handleDownload}
            class="flex items-center gap-2 px-4 py-2 bg-flame-orange hover:bg-flame-hover text-ivory-white rounded-xl text-sm font-bold transition-all cursor-pointer"
          >
            <Download size={16} />
            Download
          </button>
          <button onclick={() => closePreview()} class="text-muted-gray hover:text-ivory-white transition-colors cursor-pointer">
            <X size={20} />
          </button>
        </div>
      </div>
      <div class="flex-1 min-h-0 bg-white">
        <object
          data={previewBlobUrl}
          type="application/pdf"
          class="w-full h-full"
        >
          <div class="flex items-center justify-center h-full bg-surface-charcoal">
            <p class="text-muted-gray">PDF preview not available. <button onclick={handleDownload} class="text-flame-orange underline cursor-pointer">Download instead</button></p>
          </div>
        </object>
      </div>
    </div>
  </div>
{/if}
