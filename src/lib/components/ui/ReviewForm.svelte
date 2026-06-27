<script lang="ts">
  import { Star, Send, Loader2 } from "@lucide/svelte";
  import { toast } from "svelte-sonner";
  import { api } from "$lib/api";

  interface Props {
    menuItemId: number;
    menuItemName: string;
    onSuccess: () => void;
  }

  let { menuItemId, menuItemName, onSuccess }: Props = $props();

  let rating = $state(0);
  let hoverRating = $state(0);
  let comment = $state("");
  let loading = $state(false);

  async function handleSubmit(e: Event) {
    e.preventDefault();
    if (rating === 0) {
      toast.error("Please select a rating");
      return;
    }
    loading = true;
    try {
      await api.createReview({ menu_item_id: menuItemId, rating, comment: comment || undefined });
      onSuccess();
      toast.success("Review submitted successfully");
    } catch (err: any) {
      toast.error(err.message);
    } finally {
      loading = false;
    }
  }
</script>

<form onsubmit={handleSubmit} class="bg-surface-card rounded-2xl p-5 border border-deep-border">
  <h3 class="text-ivory-white font-bold text-sm mb-1">Review {menuItemName}</h3>

  <div class="flex gap-1 mb-3">
    {#each [1, 2, 3, 4, 5] as star}
      <button
        type="button"
        onclick={() => { rating = star; hoverRating = 0; }}
        onmouseenter={() => { hoverRating = star; }}
        onmouseleave={() => { hoverRating = 0; }}
        class="cursor-pointer"
      >
        <Star
          size={20}
          class={(hoverRating || rating) >= star ? "text-flame-orange" : "text-muted-gray"}
          fill={(hoverRating || rating) >= star ? "currentColor" : "none"}
        />
      </button>
    {/each}
  </div>

  <textarea
    bind:value={comment}
    placeholder="Share your experience (optional)"
    class="w-full bg-surface-charcoal border border-deep-border rounded-xl px-3 py-2 text-sm text-ivory-white outline-none focus:border-flame-orange resize-none"
    rows={2}
  ></textarea>

  <button
    type="submit"
    disabled={loading || rating === 0}
    class="mt-3 bg-flame-orange hover:bg-flame-hover text-ivory-white px-4 py-2 rounded-full text-sm font-bold transition-all flex items-center gap-2 disabled:opacity-50 cursor-pointer"
  >
    {#if loading}
      <Loader2 size={14} class="animate-spin" />
      Submitting...
    {:else}
      <Send size={14} />
      Submit Review
    {/if}
  </button>
</form>
