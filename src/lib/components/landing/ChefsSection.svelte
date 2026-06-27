<script lang="ts">
  import SectionHeading from "$lib/components/ui/SectionHeading.svelte";
</script>

<section class="px-gutter mb-section-gap">
  <div class="max-w-grid-max-width mx-auto">
    <div class="mb-12 text-center md:text-left">
      <SectionHeading prefix="Meet Our" highlight="Chefs" />
    </div>
    <div class="grid grid-cols-1 md:grid-cols-2 gap-0 bg-surface-charcoal rounded-[40px] overflow-hidden items-stretch">
      <div class="relative h-[400px] md:h-auto overflow-hidden">
        <img
          class="absolute inset-0 w-full h-full object-cover scale-110"
          alt="Master chef"
          src="https://lh3.googleusercontent.com/aida-public/AB6AXuAgWAcqsBOJr2IIIPnZ5FyMUGvYApzNv1iBaXAdRsmNAmlZMbvURtSRggvUPt6mREqqL_Y65sG72epvmhXBk9rTLVDuTBoaxaEhj5z4AsKEc0DRB21jyqrM1N9tVhNGTZaNDIh9HyVAyPZPKv6JCSJETCbGTnhGLGh8gefQB6wvjKvtSVH3J6n65RW84lxMClU5uLbB-QiQSCbKbhmDN4uE1V1bpJcYueGRS31PgVmDSiH4l1cWuK-KITKHRb8YsYVZfRxyLSyuj6M"
        />
        <div class="absolute inset-0 bg-gradient-to-r from-transparent to-surface-charcoal hidden md:block"></div>
      </div>
      <div class="p-8 md:p-16 flex flex-col justify-center">
        <p class="font-body-lg text-body-lg text-muted-gray mb-10 leading-relaxed">
          Our expert chefs bring passion, skill, and creativity to every
          dish, ensuring an unforgettable dining experience. With years of
          experience and a love for flavors, they craft each meal to
          perfection, using only the finest ingredients sourced globally.
        </p>
        <button class="border-2 border-flame-orange text-flame-orange px-10 py-3 rounded-full font-bold self-start hover:bg-flame-orange hover:text-white transition-all uppercase tracking-widest text-xs cursor-pointer">
          View All
        </button>
      </div>
    </div>
  </div>
</section>
