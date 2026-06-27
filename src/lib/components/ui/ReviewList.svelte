<script lang="ts">
  import StarRating from "./StarRating.svelte";

  interface Review {
    id: number;
    full_name: string;
    rating: number;
    comment?: string | null;
    created_at: string;
  }

  let { reviews = [] }: { reviews?: Review[] } = $props();
</script>

{#if reviews.length === 0}
  <p class="text-muted-gray text-sm">No reviews yet.</p>
{:else}
  <div class="space-y-3">
    {#each reviews as review}
      <div class="bg-surface-charcoal rounded-xl p-4 border border-deep-border">
        <div class="flex items-center justify-between mb-1">
          <div class="flex items-center gap-2">
            <span class="text-ivory-white font-medium text-sm">{review.full_name}</span>
            <StarRating value={review.rating} size={12} />
          </div>
          <span class="text-muted-gray text-xs">{new Date(review.created_at).toLocaleDateString("id-ID")}</span>
        </div>
        {#if review.comment}
          <p class="text-muted-gray text-xs mt-1">{review.comment}</p>
        {/if}
      </div>
    {/each}
  </div>
{/if}
