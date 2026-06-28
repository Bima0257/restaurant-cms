<script lang="ts">
  import { Bird, AtSign, Camera, Share2 } from "@lucide/svelte";

  const quickLinks = ["Home", "About Us", "Services", "Portfolio", "Testimonials"];
  const policyLinks = ["Policy Updates", "Party Sharing", "Our Rights", "Data Protection Information"];
</script>

<footer class="bg-surface-container-lowest py-12 md:py-section-gap border-t border-deep-border px-gutter">
  <div class="grid grid-cols-1 md:grid-cols-4 gap-gutter max-w-grid-max-width mx-auto">
    <div class="flex flex-col gap-6">
      <div class="font-headline-h3 text-headline-h3 text-flame-orange font-bold">WorldPlate</div>
      <p class="text-muted-gray text-sm">
        At WorldPlate, we're always excited to hear from you. Whether you
        have a project in mind or just want to chat about how we can bring
        your ideas to life.
      </p>
      <div class="flex gap-3">
        <button class="w-8 h-8 rounded-lg bg-flame-orange flex items-center justify-center text-white hover:opacity-80 transition-opacity cursor-pointer">
          <Bird size={14} />
        </button>
        <button class="w-8 h-8 rounded-lg bg-flame-orange flex items-center justify-center text-white hover:opacity-80 transition-opacity cursor-pointer">
          <AtSign size={14} />
        </button>
        <button class="w-8 h-8 rounded-lg bg-flame-orange flex items-center justify-center text-white hover:opacity-80 transition-opacity cursor-pointer">
          <Camera size={14} />
        </button>
        <button class="w-8 h-8 rounded-lg bg-flame-orange flex items-center justify-center text-white hover:opacity-80 transition-opacity cursor-pointer">
          <Share2 size={14} />
        </button>
      </div>
    </div>
    <div>
      <h5 class="text-ivory-white font-bold mb-6">Quick Links</h5>
      <ul class="flex flex-col gap-3">
        {#each quickLinks as link}
          <li>
            <a class="text-muted-gray hover:text-flame-orange transition-colors" href="/">{link}</a>
          </li>
        {/each}
      </ul>
    </div>
    <div>
      <h5 class="text-ivory-white font-bold mb-6">Policy Links</h5>
      <ul class="flex flex-col gap-3">
        {#each policyLinks as link}
          <li>
            <a class="text-muted-gray hover:text-flame-orange transition-colors" href="/">{link}</a>
          </li>
        {/each}
      </ul>
    </div>
    <div>
      <h5 class="text-ivory-white font-bold mb-6">Sign Up Our Newsletters</h5>
      <p class="text-muted-gray text-sm mb-4">Let's Stay Connected and Collaborate</p>
      <form class="flex flex-col gap-3">
        <input
          class="bg-surface-charcoal border border-deep-border rounded-xl px-4 py-3 text-sm focus:border-flame-orange focus:ring-0 outline-none"
          placeholder="Enter your email"
          type="email"
        />
        <button class="bg-flame-orange hover:bg-flame-hover text-white py-3 rounded-xl font-bold transition-all cursor-pointer" type="submit">
          Subscribe Now
        </button>
      </form>
    </div>
  </div>
  <div class="max-w-grid-max-width mx-auto mt-12 md:mt-20 pt-8 border-t border-deep-border text-center text-muted-gray text-xs">
    &copy; 2025 WorldPlate. All Rights Reserved.
  </div>
</footer>
