<script lang="ts">
  import { FileText, Download, Loader2, Calendar } from "@lucide/svelte";
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

  async function handleDownload(reportType: string) {
    loading = reportType;
    try {
      const params: Record<string, string> = {};
      if (startDate) params.start_date = startDate;
      if (endDate) params.end_date = endDate;
      await api.downloadReport(reportType, params);
    } catch (err: any) {
      toast.error(err.message);
    } finally {
      loading = null;
    }
  }
</script>

<div class="p-6 max-w-4xl mx-auto">
  <div class="mb-6">
    <h1 class="font-headline-h3 text-headline-h3 text-ivory-white">Reports</h1>
    <p class="text-muted-gray text-sm mt-1">Generate and download PDF reports</p>
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
            onclick={() => handleDownload(report.id)}
            disabled={loading !== null}
            class="bg-flame-orange hover:bg-flame-hover text-ivory-white p-2.5 rounded-xl transition-all disabled:opacity-50 cursor-pointer shrink-0"
          >
            {#if loading === report.id}
              <Loader2 size={16} class="animate-spin" />
            {:else}
              <Download size={16} />
            {/if}
          </button>
        </div>
      </div>
    {/each}
  </div>
</div>
