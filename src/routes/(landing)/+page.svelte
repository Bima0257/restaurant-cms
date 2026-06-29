<script lang="ts">
  import { onMount } from "svelte";
  import { goto } from "$app/navigation";
  import { auth } from "$lib/stores/auth";
  import { get } from "svelte/store";
  import Hero from "$lib/components/landing/Hero.svelte";
  import PromoBanner from "$lib/components/landing/PromoBanner.svelte";
  import FeaturedSection from "$lib/components/landing/FeaturedSection.svelte";
  import MenuGrid from "$lib/components/landing/MenuGrid.svelte";
  import Testimonials from "$lib/components/landing/Testimonials.svelte";
  import ChefsSection from "$lib/components/landing/ChefsSection.svelte";

  onMount(() => {
    const user = get(auth);
    if (user && user.role === "customer") {
      goto("/dashboard");
    }
  });
</script>

<Hero />
<PromoBanner />
<FeaturedSection />
<MenuGrid />
<Testimonials />
<ChefsSection />
