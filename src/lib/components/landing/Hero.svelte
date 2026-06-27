<script lang="ts">
  import { Play } from "@lucide/svelte";
  import AvatarGroup from "$lib/components/ui/AvatarGroup.svelte";

  const avatars = [
    { src: "https://lh3.googleusercontent.com/aida-public/AB6AXuC8vM5XbMjoYc8uqXdht-Tl_oQo8GTar7Dx8X_s22py_urdkDramJwvklLbsaFI_4Swbqm-ck9lURSclAet4hFboaKVTU11rq_nzNDyz73AMx9yCnqcAf4wB5rH-P75Z2V0T83dY3CNes387rB5QaVHnQXHzSmLPZaVNdK1Socy_pWsrnIm-Kwy0-DnfvvQcnb3MxpK77DY4xWxXdlH8wODKuBT58g--1YnWu-GSkB0q_YTZjN1AwZrACo9V4c6MafGBHTCNOY5wL0" },
    { src: "https://lh3.googleusercontent.com/aida-public/AB6AXuCvNXHduzX4Uw30hNAWwJHf2VWqQ2pk9rBUDtEcjEaDnzUsBkyfnP-YIPcfsZENEg014uHKqpygvDSSP0agbxkPnR9PdUG97NcX--FomP-fXZYzPD3FDMVPdcfxIx6Mo93rQBv2kh7nPdn0FxqSOb5wnywCdmNfoo-AQexnUHqb81a3VAFNT_8U-Z8npJJFxPN1nwCwueP_BtMNQ4RVWsHgP6r3NspP4NQbH0A7KVI_hHVAKv-EDv6Go376q-OTq8G8MTC_CictW0Q" },
    { src: "https://lh3.googleusercontent.com/aida-public/AB6AXuC6trBSdD2JFRS-hgcslqQcszejiQStRV_b1lPdYou8x6UragDVqyXbl9OcQ4dEYgXIUKL-ehBlQTgAFW2t2_J_I9f9_chr47PzgmuKriLXBZYklREftIyh-UVCxH24hf-13JCFMB0nQkwG7_kcUMph_1iTN8hsvnm3rGBygTdGHY6hRA4dgE96hp2BXdERd0EAI7kL5UgKbT6HMCTOStCGQ5HeVyLsZYyoJ-MatnFh4WJewPDzMXp7UKXxQUrY8XnneERMofOHEV0" },
  ];
</script>

<header class="relative pt-32 pb-20 md:pt-48 md:pb-32 px-gutter overflow-visible max-w-grid-max-width mx-auto">
  <div class="grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
    <div class="z-10">
      <h1 class="font-hero-mobile md:font-hero-lg text-hero-mobile md:text-hero-lg mb-6 leading-tight">
        Experience the <br />
        <span class="text-flame-orange italic">Taste</span> of the <br />
        World
      </h1>
      <p class="font-body-lg text-body-lg text-muted-gray mb-10 max-w-md">
        From classic favorites to exotic delights, explore a diverse menu
        inspired by cuisines from across the globe.
      </p>
      <div class="flex gap-4 items-center flex-wrap">
        <button class="bg-flame-orange hover:bg-flame-hover text-ivory-white px-8 py-4 rounded-full font-bold flex items-center gap-2 orange-glow transition-all transform hover:scale-105 cursor-pointer">
          Learn More
          <Play size={16} fill="currentColor" />
        </button>
        <div class="flex items-center gap-3">
          <AvatarGroup {avatars} size="sm" />
          <span class="text-muted-gray text-sm font-medium">Happy Customers</span>
        </div>
      </div>
    </div>
    <div class="relative flex justify-center items-center">
      <div class="absolute w-[120%] h-[120%] bg-flame-orange/5 blur-[120px] rounded-full"></div>
      <img
        class="w-full max-w-md md:max-w-xl object-contain floating-anim food-shadow"
        alt="steaming bowl of ramen"
        src="https://lh3.googleusercontent.com/aida-public/AB6AXuB7pvqy-Ka9TNOM1jEOzPRGoVI_y2Zu-RC5ERYiWIQI8FbrR9GSp9_I4tyD_m4twYncUjyPIZ6C6EhZVG35E3d5c8q__6ptvxAjml3Y2xTE4r80_yVNxmQNmwdSD8dxcbXS5dCKhs0iC9hJ526w6tAYFjamokX-3oDiJXQc9EmUYbjZ50EU4JdceBdk2ekZBQDTt5styPLczvU4Y1LFl9C5RkYewd3ixjHFr8_EfuC9hoQFb9NJdyT144-PjOXBHeVqY-RWhSQcTZc"
      />
    </div>
  </div>
</header>
