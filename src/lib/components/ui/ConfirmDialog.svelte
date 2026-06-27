<script lang="ts">
  import { getDialogState } from "$lib/utils/confirm";

  const dialog = getDialogState();
  let dialogState = $state<{
    title: string;
    message: string;
    confirmLabel: string;
    cancelLabel: string;
    variant: "danger" | "primary";
    resolve: (value: boolean) => void;
    open: boolean;
  } | null>(null);

  dialog.subscribe((value) => {
    dialogState = value;
  });
</script>

{#if dialogState}
  <!-- svelte-ignore a11y_no_static_element_interactions -->
  <div
    class="fixed inset-0 bg-black/60 flex items-center justify-center z-[9999] p-4"
    onclick={dialog.cancel}
    onkeydown={(e) => { if (e.key === "Escape") dialog.cancel(); }}
    role="dialog"
    aria-modal="true"
    tabindex="-1"
  >
    <!-- svelte-ignore a11y_no_static_element_interactions -->
    <div
      class="bg-surface-card rounded-3xl p-6 w-full max-w-md"
      onclick={(e: Event) => e.stopPropagation()}
      onkeydown={() => {}}
    >
      <h2 class="text-ivory-white font-bold text-lg text-center mb-2">
        {dialogState.title}
      </h2>
      <p class="text-muted-gray text-sm text-center mb-6">
        {dialogState.message}
      </p>
      <div class="flex gap-3">
        <button
          onclick={dialog.cancel}
          class="flex-1 bg-surface-charcoal hover:bg-deep-border text-ivory-white py-2.5 rounded-full font-bold text-sm transition-all cursor-pointer"
        >
          {dialogState.cancelLabel}
        </button>
        <button
          onclick={dialog.confirm}
          class={dialogState.variant === "danger"
            ? "flex-1 bg-red-500 hover:bg-red-600 text-white py-2.5 rounded-full font-bold text-sm transition-all cursor-pointer"
            : "flex-1 bg-flame-orange hover:bg-flame-hover text-ivory-white py-2.5 rounded-full font-bold text-sm transition-all cursor-pointer"}
        >
          {dialogState.confirmLabel}
        </button>
      </div>
    </div>
  </div>
{/if}
