<script lang="ts">
  import SectionHeading from "$lib/components/ui/SectionHeading.svelte";
  import StarRating from "$lib/components/ui/StarRating.svelte";

  const testimonials = [
    {
      name: "John Smith",
      avatar: "https://lh3.googleusercontent.com/aida-public/AB6AXuB2tC54FW8sqfWZLkiCwBHLtdS_lerOU1-a9I_Kmn8J9UaDvRl6D_g-gDWWlR3VgAXg8t_IRzdkFCTw0Gp8tUAwqIY_tLePH1BWQ4chIHGtr48CPaNmVcraWhuUtaQZLF-LG0hVOnl2s_thTGIO7ixMyW1ZxDWDWorg4d-0K5LLKqSgmAdK2V-c3xiPLrZ_42h9c8OCxbQdElhRiPzyiqeMJ5hqChHEjLFtKLON4UyY85YDskbvIOeBUqMpb4OF8ZqTmcaUgNwAXGA",
      rating: 5,
      text: "\"Absolutely loved the flavors! The food was fresh, and the delivery was super fast. Highly recommend this for fine dining at home.\"",
    },
    {
      name: "Michael Chen",
      avatar: "https://lh3.googleusercontent.com/aida-public/AB6AXuAoKVApVnmyzOBE2MTpv985ilCA2ro0sH1GvwiWifUCSvdLftTUwuwxBb2frjQQpXvGkn83WfS3Lhu2AJQGp66_gSPDMddhiq7U4kXg8OjDKb_37ieTeARahNECCLpDyk_ADn2fCF9RZVsJcPXzWvSAh6tnDJA6hucxBsUxF7cqxSUNzLbrjQg36iyAa3Rr0Ka9uZ3GR6NgAtzTRgtBt8fusy5EmZjtVxdldpBdBeTyvnobZ_rGlNdN3Oz7kmRZHjtYlZEoWiY-0mM",
      rating: 5,
      text: "\"The ramen is authentic and packed with depth. It's rare to find such high-quality ingredients in a delivery service.\"",
    },
    {
      name: "Sarah Williams",
      avatar: "https://lh3.googleusercontent.com/aida-public/AB6AXuDpRmx1cGbkBTMIXjZUY7m_qHt9uFadfA773znl5EQNj0B9zWLMMHYFftKNqb08ss83JHydTJZ-7J9Aa25GU9x0RGtTqzNulH_pdgfX1L8D-dMsId-V6vWLxJUYh3DvxWf8LWsSR118WmPerFtDDSdiuk1e-nKGVnYVT3Tgqp5MK48ugr_5Bd-AWrUP2KmqT7XUSROuLfDO8JiCazDaxnHTlTZ6C2mxNj3f0w7bFRVcf3AAmG535FxmeUkz44_cejiSBmF8K1zzw9w",
      rating: 5,
      text: "\"The presentation was stunning, even in the packaging. You can tell the chefs really care about the craft.\"",
    },
  ];
</script>

<section class="px-gutter mb-section-gap relative py-20 overflow-hidden">
  <div class="absolute inset-0 z-0 opacity-20">
    <img
      class="w-full h-full object-cover"
      alt="testimonial background"
      src="https://lh3.googleusercontent.com/aida-public/AB6AXuBIN_k4sZT9cwCMXeYGDXnEJpT90_9oJhIDZLRvBYBj1bRwfZqYBieJFNROmmlU7DTNpitPdx1meK9xrOOeerphpwKjRNpIyXziwi1QmOjIA2LmkYEhKJM60zmNegi__MuM6ywh-Abkwskv7u2dRu5_lfMYPRiDxplszmbzWdLWN5CgKN64PLVGMj6bVrh-z8cY8IDTz4Si24rxF92YiLBaG6yYmpx-Ca3yaioItivqc_vKSl8DvoOpTvmhFwq9tvyESqE1EHWWurY"
    />
  </div>
  <div class="max-w-grid-max-width mx-auto relative z-10">
    <div class="text-center mb-16">
      <SectionHeading prefix="What They" highlight="Say?" />
    </div>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      {#each testimonials as t}
        <div class="bg-surface/60 backdrop-blur-xl p-8 rounded-3xl border border-white/5">
          <div class="flex items-center gap-4 mb-4">
            <img
              class="w-12 h-12 rounded-full object-cover border-2 border-flame-orange"
              src={t.avatar}
              alt={t.name}
            />
            <div>
              <div class="font-bold">{t.name}</div>
              <StarRating value={t.rating} size={14} />
            </div>
          </div>
          <p class="text-muted-gray text-sm leading-relaxed">{t.text}</p>
        </div>
      {/each}
    </div>
  </div>
</section>
