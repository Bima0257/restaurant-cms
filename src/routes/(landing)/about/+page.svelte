<script lang="ts">
  import SectionHeading from "$lib/components/ui/SectionHeading.svelte";
  import ChefsSection from "$lib/components/landing/ChefsSection.svelte";
</script>

<div class="pt-32 pb-20 px-gutter max-w-grid-max-width mx-auto">
  <div class="mb-16">
    <SectionHeading prefix="About" highlight="WorldPlate" />
  </div>
  <div class="grid grid-cols-1 md:grid-cols-2 gap-12 items-center mb-20">
    <div>
      <p class="font-body-lg text-body-lg text-muted-gray mb-6 leading-relaxed">
        WorldPlate was founded with a simple mission: to bring the finest global cuisines to your doorstep.
        We believe that food is more than just sustenance — it's an experience, a journey, and a celebration of culture.
      </p>
      <p class="font-body-lg text-body-lg text-muted-gray mb-6 leading-relaxed">
        Our chefs travel the world to bring you authentic recipes, using only the freshest ingredients sourced from local farmers and international markets.
      </p>
      <p class="font-body-lg text-body-lg text-muted-gray leading-relaxed">
        Whether you're craving a classic Italian pizza, a hearty American burger, or delicate Japanese sushi, WorldPlate delivers an unforgettable dining experience right to your home.
      </p>
    </div>
    <div class="relative">
      <div class="absolute w-[120%] h-[120%] bg-flame-orange/5 blur-[120px] rounded-full"></div>
      <img
        class="w-full rounded-[40px] food-shadow"
        alt="WorldPlate kitchen"
        src="https://images.unsplash.com/photo-1556910103-1c02745aae4d?w=800"
      />
    </div>
  </div>
  <ChefsSection />
</div>
