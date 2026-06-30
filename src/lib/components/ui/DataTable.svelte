<script lang="ts">
  import { Pencil, Trash2, Loader2, ChevronUp, ChevronDown, ChevronLeft, ChevronRight } from "@lucide/svelte";
  import { createTable, FlexRender } from "@tanstack/svelte-table";
  import {
    rowSortingFeature,
    rowPaginationFeature,
    createSortedRowModel,
    createPaginatedRowModel,
    createCoreRowModel,
  } from "@tanstack/table-core";
  import type { SortingState, PaginationState } from "@tanstack/table-core";
  import type { Snippet } from "svelte";

  let {
    columns,
    rows,
    onEdit,
    onDelete,
    onRowClick,
    loading = false,
    emptyMessage = "No data found",
    class: className = "",
    cell,
    actions,
    pageSize = 10,
  }: {
    columns: { key: string; label: string; sortable?: boolean }[];
    rows: Record<string, any>[];
    onEdit?: (row: Record<string, any>) => void;
    onDelete?: (row: Record<string, any>) => void;
    onRowClick?: (row: Record<string, any>) => void;
    loading?: boolean;
    emptyMessage?: string;
    class?: string;
    cell?: Snippet<[{ col: { key: string; label: string; sortable?: boolean }; row: Record<string, any>; value: any }]>;
    actions?: Snippet<[{ row: Record<string, any> }]>;
    pageSize?: number;
  } = $props();

  let hasActions = $derived(!!(onEdit || onDelete || actions));

  let sorting = $state<SortingState>([]);
  let paginationState = $state<PaginationState>({ pageIndex: 0, pageSize });

  let tableColumns = $derived(
    columns.map((col) => ({
      accessorKey: col.key,
      id: col.key,
      header: col.label,
      enableSorting: col.sortable ?? true,
    }))
  );

  let table = createTable(
    {
      features: {
        rowSortingFeature,
        rowPaginationFeature,
        sortedRowModel: createSortedRowModel(),
        paginatedRowModel: createPaginatedRowModel(),
        coreRowModel: createCoreRowModel(),
      },
      get columns() { return tableColumns; },
      get data() { return rows; },
      state: {
        get sorting() { return sorting; },
        get pagination() { return paginationState; },
      },
      onSortingChange: (updater: any) => {
        sorting = typeof updater === "function" ? updater(sorting) : updater;
      },
      onPaginationChange: (updater: any) => {
        paginationState = typeof updater === "function" ? updater(paginationState) : updater;
      },
    } as any
  );

  function pageNumbers(): (number | "...")[] {
    const total: number = (table as any).getPageCount();
    const cur = paginationState.pageIndex;
    if (total <= 7) return Array.from({ length: total }, (_, i) => i);

    const pages: (number | "...")[] = [0];
    if (cur > 3) pages.push("...");

    const start = Math.max(1, cur - 1);
    const end = Math.min(total - 2, cur + 1);
    for (let i = start; i <= end; i++) pages.push(i);

    if (cur < total - 4) pages.push("...");
    pages.push(total - 1);
    return pages;
  }

  const totalColumns = columns.length + (hasActions ? 1 : 0);
</script>

<div class="overflow-x-auto {className}">
  <table class="w-full text-sm">
    <thead>
      <tr class="border-b border-deep-border">
        {#each (table as any).getHeaderGroups()[0].headers as header}
          <th class="text-left py-3 px-4 text-muted-gray font-medium">
            {#if (header.column as any).getCanSort()}
              <button
                class="flex items-center gap-1 hover:text-ivory-white transition-colors cursor-pointer"
                onclick={() => (header.column as any).toggleSorting()}
              >
                <FlexRender header={header} />
                {#if (header.column as any).getIsSorted() === "asc"}
                  <ChevronUp size={14} class="text-flame-orange" />
                {:else if (header.column as any).getIsSorted() === "desc"}
                  <ChevronDown size={14} class="text-flame-orange" />
                {/if}
              </button>
            {:else}
              <span><FlexRender header={header} /></span>
            {/if}
          </th>
        {/each}
        {#if hasActions}
          <th class="text-right py-3 px-4 text-muted-gray font-medium">Actions</th>
        {/if}
      </tr>
    </thead>
    <tbody>
      {#if loading}
        <tr>
          <td colspan={totalColumns} class="py-12 text-center">
            <Loader2 size={24} class="animate-spin text-muted-gray mx-auto" />
            <p class="text-muted-gray text-sm mt-2">Loading...</p>
          </td>
        </tr>
      {:else if rows.length === 0}
        <tr>
          <td colspan={totalColumns} class="py-12 text-center text-muted-gray">
            {emptyMessage}
          </td>
        </tr>
      {:else}
        {#each (table as any).getRowModel().rows as row}
          <tr
            class="border-b border-deep-border hover:bg-surface-charcoal/50 transition-colors {onRowClick ? 'cursor-pointer' : ''}"
            onclick={() => onRowClick?.(row.original)}
            onkeydown={(e) => { if (e.key === "Enter") onRowClick?.(row.original); }}
            role={onRowClick ? "button" : undefined}
            tabindex={onRowClick ? 0 : undefined}
          >
            {#each (row as any).getAllCells() as tanstackCell, i}
              <td class="py-3 px-4 text-ivory-white">
                {#if cell}
                  {@render cell({ col: columns[i], row: row.original, value: (tanstackCell as any).getValue() })}
                {:else}
                  {(tanstackCell as any).getValue()}
                {/if}
              </td>
            {/each}
            {#if hasActions}
              <td class="py-3 px-4 text-right">
                {#if actions}
                  {@render actions({ row: row.original })}
                {:else}
                  <div class="flex items-center justify-end gap-2">
                    {#if onEdit}
                      <button onclick={(e) => { e.stopPropagation(); onEdit(row.original); }} class="p-1.5 rounded-lg hover:bg-flame-orange/10 text-muted-gray hover:text-flame-orange transition-colors cursor-pointer">
                        <Pencil size={14} />
                      </button>
                    {/if}
                    {#if onDelete}
                      <button onclick={(e) => { e.stopPropagation(); onDelete(row.original); }} class="p-1.5 rounded-lg hover:bg-red-500/10 text-muted-gray hover:text-red-400 transition-colors cursor-pointer">
                        <Trash2 size={14} />
                      </button>
                    {/if}
                  </div>
                {/if}
              </td>
            {/if}
          </tr>
        {/each}
      {/if}
    </tbody>
  </table>
</div>

{#if (table as any).getPageCount() > 1 && rows.length > 0 && !loading}
  <div class="flex items-center justify-between mt-4 pt-4 border-t border-deep-border">
    <div class="flex items-center gap-2 text-sm text-muted-gray">
      <span>Rows per page:</span>
      <select
        class="bg-surface-charcoal border border-deep-border rounded-lg px-2 py-1 text-sm text-ivory-white cursor-pointer"
        value={paginationState.pageSize}
        onchange={(e) => {
          const target = e.currentTarget as HTMLSelectElement;
          (table as any).setPageSize(Number(target.value));
        }}
      >
        {#each [10, 20, 50, 100] as size}
          <option value={size}>{size}</option>
        {/each}
      </select>
    </div>
    <div class="flex items-center gap-1">
      <button
        onclick={() => (table as any).previousPage()}
        disabled={!(table as any).getCanPreviousPage()}
        class="p-1.5 rounded-lg hover:bg-surface-charcoal text-muted-gray hover:text-ivory-white disabled:opacity-30 disabled:cursor-not-allowed transition-colors cursor-pointer"
      >
        <ChevronLeft size={16} />
      </button>
      {#each pageNumbers() as p}
        {#if p === "..."}
          <span class="px-2 text-muted-gray">...</span>
        {:else}
          <button
            onclick={() => (table as any).setPageIndex(p)}
            class="min-w-[32px] h-8 rounded-lg text-sm font-medium transition-colors cursor-pointer {p === paginationState.pageIndex ? 'bg-flame-orange text-ivory-white' : 'text-muted-gray hover:bg-surface-charcoal hover:text-ivory-white'}"
          >
            {p + 1}
          </button>
        {/if}
      {/each}
      <button
        onclick={() => (table as any).nextPage()}
        disabled={!(table as any).getCanNextPage()}
        class="p-1.5 rounded-lg hover:bg-surface-charcoal text-muted-gray hover:text-ivory-white disabled:opacity-30 disabled:cursor-not-allowed transition-colors cursor-pointer"
      >
        <ChevronRight size={16} />
      </button>
    </div>
  </div>
{/if}
