<script lang="ts">
  import { Plus, Star } from "@lucide/svelte";
  import Card from "$lib/components/ui/Card.svelte";

  let {
    image,
    title,
    description,
    price,
    rating = 0,
  }: {
    image: string;
    title: string;
    description: string;
    price: string;
    rating?: number;
  } = $props();
</script>

<Card>
  <div class="relative mb-6">
    <img
      class="w-full h-64 object-cover rounded-2xl mb-4"
      alt={title}
      src={image}
    />
    <button class="absolute bottom-4 right-4 bg-flame-orange text-white w-10 h-10 rounded-full flex items-center justify-center hover:scale-110 transition-transform cursor-pointer">
      <Plus size={20} />
    </button>
  </div>
  <h4 class="font-headline-h3 text-headline-h3 mb-2">{title}</h4>
  <p class="text-muted-gray text-sm mb-4">{description}</p>
  <div class="flex justify-between items-center">
    <span class="font-label-price text-label-price">{price}</span>
    <div class="flex gap-1">
      {#each Array(5) as _, i}
        <Star
          size={12}
          class={i < rating ? "text-flame-orange" : "text-muted-gray"}
          fill={i < rating ? "currentColor" : "none"}
        />
      {/each}
    </div>
  </div>
</Card>
