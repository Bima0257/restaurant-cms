<script lang="ts">
  import SectionHeading from "$lib/components/ui/SectionHeading.svelte";
  import MenuCard from "$lib/components/landing/MenuCard.svelte";

  const allMenu = [
    { image: "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=800", title: "Margherita Pizza", description: "Best Chicken and beef mix with tomato fresh from the farm.", price: "$19.00", rating: 4 },
    { image: "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=800", title: "Signature Burger", description: "Double patties, melted gouda, and our secret WorldPlate sauce.", price: "$24.00", rating: 5 },
    { image: "https://images.unsplash.com/photo-1579871494447-9811cf80d66c?w=800", title: "Salmon Sushi Set", description: "Fresh Atlantic salmon with premium wasabi and ginger.", price: "$32.00", rating: 4 },
    { image: "https://images.unsplash.com/photo-1533089860892-a7c6f0a88666?w=800", title: "Breakfast Specials", description: "Fluffy scrambled eggs, crispy bacon, artisan toast.", price: "$99.00", rating: 5 },
    { image: "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=800", title: "Ramen Bowl", description: "Golden-brown broth with wavy noodles, soft-boiled egg.", price: "$28.00", rating: 5 },
    { image: "https://images.unsplash.com/photo-1604382354936-07c5d9983bd3?w=800", title: "Wood-Fired Pizza", description: "Bubbling mozzarella with fresh basil on charred crust.", price: "$22.00", rating: 4 },
  ];
</script>

<div class="pt-32 pb-20 px-gutter max-w-grid-max-width mx-auto">
  <div class="mb-12">
    <SectionHeading prefix="Our" highlight="Menu" />
  </div>
  <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
    {#each allMenu as item}
      <MenuCard {...item} />
    {/each}
  </div>
</div>
