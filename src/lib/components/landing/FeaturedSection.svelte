<script lang="ts">
  import SectionHeading from "$lib/components/ui/SectionHeading.svelte";
  import { ShoppingBasket } from "@lucide/svelte";
</script>

<section class="px-gutter mb-section-gap relative">
  <div class="max-w-grid-max-width mx-auto">
    <div class="mb-12">
      <SectionHeading prefix="Our Best" highlight="Delivered" />
    </div>
    <div class="relative bg-surface-charcoal rounded-[40px] p-8 md:p-16 overflow-hidden flex flex-col md:flex-row items-center gap-12 group">
      <div class="relative w-full md:w-1/2">
        <img
          class="w-full h-auto scale-110 -translate-x-0 md:-translate-x-24 food-shadow"
          alt="Breakfast specials"
          src="https://lh3.googleusercontent.com/aida-public/AB6AXuAqZEXonZBQu4cmGT_WFtDqyMaDYET5PthRxfVN3rK590_hyUuZetM4sMmRLyt2NWYxiv7vcztKJISzvK0Vpd0FIYkF8zg87r9vbrMALvQPMrNDrzg_PJFZGVM4lQdlgXT8LFQLWfkwLSrHCsnZpMW_UXGAMUJpgNuXhMbGM_pvxSIaHGESYdPm5GvSyA_GJK0OpkuAYA9qxbB7GKODJsDvweHkaj6S6GZJBniI-Eqhi74ifqltdoRJtrE5tVzo5fxFwhtgHfq4SfI"
        />
      </div>
      <div class="w-full md:w-1/2 z-10">
        <h3 class="font-headline-h1 text-headline-h1 mb-4">Breakfast Specials</h3>
        <p class="font-body-lg text-body-lg text-muted-gray mb-8">
          Explore our top-rated food categories, crafted to satisfy every
          craving! From delicious breakfasts that jumpstart your morning.
        </p>
        <div class="font-label-price text-[48px] text-ivory-white mb-8">$99/-</div>
        <div class="flex gap-4">
          <button class="bg-flame-orange hover:bg-flame-hover text-ivory-white px-6 md:px-10 py-3 md:py-4 rounded-full font-bold transition-all hover:px-8 md:hover:px-12 cursor-pointer text-sm md:text-base">
            Order Now
          </button>
          <button class="bg-surface-container-lowest hover:bg-surface-bright text-flame-orange w-14 h-14 rounded-full flex items-center justify-center transition-transform hover:scale-110 cursor-pointer">
            <ShoppingBasket size={24} />
          </button>
        </div>
      </div>
    </div>
  </div>
</section>
