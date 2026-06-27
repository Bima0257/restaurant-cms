<script lang="ts">
  import AvatarGroup from "$lib/components/ui/AvatarGroup.svelte";

  const avatars = [
    { src: "https://lh3.googleusercontent.com/aida-public/AB6AXuC2trliTLNIoKmgP9yao03ndiv8hCn8RrcUMDES7cSPqC8Ht24m3lLXK-Ak68Jf7P5YKoWbm90JadsVVUqmKrpri3IgqOSMLKJzOqFSVo6rdxtv70RYYlBwrV24LoWqJgXzzAD0AMaVPOcdqUt1RaBBvDibn7Tbt8PQnQm_rJl2F4vJCuwUdx-WF3UugCcNFd2irzyYA7wDNORtw1WV1Ywu11hBrmpZdW7slo0fnRR4BNykQCW0gXqkpaqk9wNqDRjfVyRnOJ5lG3c" },
    { src: "https://lh3.googleusercontent.com/aida-public/AB6AXuD0IqcK6yzjhx6RdLOPn0AEmCA6WAkI13kk8lnnT2znjlGMqpKPt6tiX3dw_f3Wy0ON64lX9d5w1jrqzRSPyuc-gSbAp7HsLFdkc0dSaMoC6XNP_vv4YYSgdhc_PhBetBuI1Mh_G_7nVrHWjef-uSnHnzDSTUkBlXV1LnAPp1yQMxV7_kNF5b7AMBTbI07FGwq8Zwg0A50tANjl35-Gc1GbscKTR3o2igOH2v6WemiraXS5jEEROcRdy1EfjBxXNV4OWKG7TbawaEM" },
    { src: "https://lh3.googleusercontent.com/aida-public/AB6AXuCtkHgyqRE9QGANEMPKMTd-yPxbYpqq4sEeMqS8MtMNEu9oirW-HEEhmEq4QY5gGWGmvgMqA--xoWK--84UEMY6RSTtcHSQHzcGh_VUBv7JmDSzrMEcb5LU0z36AtjuZ-6ObKTuwmwD_CPfILuohDHU4putaEtXoHVdKwlLRoVTiOP6DXL7HtpUMbiii7e9i_wD0hTTTk4dgW_COkOlIE4c0Gxjpf8JKLTKeyKqaAoVLOrTfeWbsqBbEw3iVuBQ3jU0yq01wr-BvHw" },
  ];
</script>

<section class="px-gutter mb-section-gap">
  <div class="max-w-grid-max-width mx-auto">
    <div class="ticket-notch bg-white py-12 px-8 md:px-16 flex flex-col md:flex-row justify-between items-center gap-8 rounded-3xl overflow-hidden shadow-2xl">
      <div class="flex flex-col md:flex-row items-center gap-8">
        <div class="text-surface font-headline-h2 text-headline-h2 max-w-xs text-center md:text-left">
          Great food and lots of discounted prices
        </div>
        <div class="flex flex-col items-center gap-2">
          <AvatarGroup {avatars} size="sm" surplus={40} overlap={true} />
          <span class="text-muted-gray text-sm font-medium">People grabbed the offer</span>
        </div>
      </div>
      <div class="flex items-center gap-12 border-l-2 border-dashed border-gray-200 pl-0 md:pl-12">
        <div class="text-center">
          <div class="text-surface font-hero-mobile text-hero-mobile font-black">50%</div>
          <div class="text-muted-gray font-bold tracking-widest uppercase text-xs">offer on Now</div>
        </div>
        <div class="w-32 h-32 rounded-full overflow-hidden border-4 border-white shadow-xl transform rotate-12">
          <img
            class="w-full h-full object-cover"
            alt="Margherita pizza"
            src="https://lh3.googleusercontent.com/aida-public/AB6AXuCWqZT6lst83FxqHlpuPctP3JZuBOTFA-WnSqZuoW4JBTr68SipV6Z71h1_ZFiDvmrKM8lEZDS_xqaLBhLOhOfJ46ACo1HSL5IirRFbKMekTXR42bvKST6cqLnXyAK9hRn_2qtzfKBBHMhPGnb0IlkK1wkzPcPIE7cxY3Lit-Ti8hTYCG0x_zeA3gVvo8l4YIllgG2rAXsZrT3A0VPBKtClSt-0rOto3PfQIFhyz0UHDYojLAhRq6iwkdVhfDUr_G0HuxuQcbqIAiQ"
          />
        </div>
      </div>
    </div>
  </div>
</section>
