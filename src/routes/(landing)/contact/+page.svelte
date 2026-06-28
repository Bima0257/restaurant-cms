<script lang="ts">
  import SectionHeading from "$lib/components/ui/SectionHeading.svelte";
  import { MapPin, Phone, Mail, Clock } from "@lucide/svelte";
</script>

<div class="pt-24 pb-12 md:pt-32 md:pb-20 px-gutter max-w-grid-max-width mx-auto">
  <div class="mb-12">
    <SectionHeading prefix="Get In" highlight="Touch" />
  </div>
  <div class="grid grid-cols-1 md:grid-cols-2 gap-12">
    <div>
      <div class="bg-surface-card rounded-3xl p-8 mb-8">
        <h3 class="font-headline-h3 text-headline-h3 mb-6">Send us a message</h3>
        <form class="flex flex-col gap-4">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <input
              class="bg-surface-charcoal border border-deep-border rounded-xl px-4 py-3 text-sm focus:border-flame-orange focus:ring-0 outline-none text-ivory-white"
              placeholder="Your Name"
              type="text"
            />
            <input
              class="bg-surface-charcoal border border-deep-border rounded-xl px-4 py-3 text-sm focus:border-flame-orange focus:ring-0 outline-none text-ivory-white"
              placeholder="Your Email"
              type="email"
            />
          </div>
          <input
            class="bg-surface-charcoal border border-deep-border rounded-xl px-4 py-3 text-sm focus:border-flame-orange focus:ring-0 outline-none text-ivory-white"
            placeholder="Subject"
            type="text"
          />
          <textarea
            class="bg-surface-charcoal border border-deep-border rounded-xl px-4 py-3 text-sm focus:border-flame-orange focus:ring-0 outline-none text-ivory-white min-h-[120px]"
            placeholder="Your Message"
          ></textarea>
          <button class="bg-flame-orange hover:bg-flame-hover text-white py-3 rounded-full font-bold transition-all cursor-pointer">
            Send Message
          </button>
        </form>
      </div>
    </div>
    <div>
      <div class="bg-surface-card rounded-3xl p-8">
        <h3 class="font-headline-h3 text-headline-h3 mb-6">Contact Information</h3>
        <div class="flex flex-col gap-6">
          <div class="flex items-center gap-4">
            <div class="w-12 h-12 rounded-full bg-flame-orange/10 flex items-center justify-center text-flame-orange">
              <MapPin size={20} />
            </div>
            <div>
              <p class="font-bold text-ivory-white">Address</p>
              <p class="text-muted-gray text-sm">123 Gourmet Street, Food District, NY 10001</p>
            </div>
          </div>
          <div class="flex items-center gap-4">
            <div class="w-12 h-12 rounded-full bg-flame-orange/10 flex items-center justify-center text-flame-orange">
              <Phone size={20} />
            </div>
            <div>
              <p class="font-bold text-ivory-white">Phone</p>
              <p class="text-muted-gray text-sm">+1 (555) 123-4567</p>
            </div>
          </div>
          <div class="flex items-center gap-4">
            <div class="w-12 h-12 rounded-full bg-flame-orange/10 flex items-center justify-center text-flame-orange">
              <Mail size={20} />
            </div>
            <div>
              <p class="font-bold text-ivory-white">Email</p>
              <p class="text-muted-gray text-sm">hello@worldplate.com</p>
            </div>
          </div>
          <div class="flex items-center gap-4">
            <div class="w-12 h-12 rounded-full bg-flame-orange/10 flex items-center justify-center text-flame-orange">
              <Clock size={20} />
            </div>
            <div>
              <p class="font-bold text-ivory-white">Working Hours</p>
              <p class="text-muted-gray text-sm">Mon - Sun: 8:00 AM - 11:00 PM</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
