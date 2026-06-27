<script lang="ts">
  import SectionHeading from "$lib/components/ui/SectionHeading.svelte";
</script>

<div class="mb-8">
  <SectionHeading prefix="Restaurant" highlight="Settings" />
</div>

<div class="max-w-2xl space-y-6">
  <div class="bg-surface-card rounded-2xl border border-deep-border p-6">
    <h3 class="font-headline-h3 text-headline-h3 text-ivory-white mb-6">General Information</h3>
    <form class="flex flex-col gap-4">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label for="rest-name" class="block text-sm text-muted-gray mb-1">Restaurant Name</label>
          <input id="rest-name"
            class="w-full bg-surface-charcoal border border-deep-border rounded-xl px-4 py-3 text-sm focus:border-flame-orange focus:ring-0 outline-none text-ivory-white"
            type="text"
            value="WorldPlate"
          />
        </div>
        <div>
          <label for="rest-email" class="block text-sm text-muted-gray mb-1">Email</label>
          <input id="rest-email"
            class="w-full bg-surface-charcoal border border-deep-border rounded-xl px-4 py-3 text-sm focus:border-flame-orange focus:ring-0 outline-none text-ivory-white"
            type="email"
            value="hello@worldplate.com"
          />
        </div>
      </div>
      <div>
        <label for="rest-address" class="block text-sm text-muted-gray mb-1">Address</label>
        <input id="rest-address"
          class="w-full bg-surface-charcoal border border-deep-border rounded-xl px-4 py-3 text-sm focus:border-flame-orange focus:ring-0 outline-none text-ivory-white"
          type="text"
          value="123 Gourmet Street, Food District, NY 10001"
        />
      </div>
      <div>
        <label for="rest-phone" class="block text-sm text-muted-gray mb-1">Phone</label>
        <input id="rest-phone"
          class="w-full bg-surface-charcoal border border-deep-border rounded-xl px-4 py-3 text-sm focus:border-flame-orange focus:ring-0 outline-none text-ivory-white"
          type="text"
          value="+1 (555) 123-4567"
        />
      </div>
      <button class="bg-flame-orange hover:bg-flame-hover text-ivory-white py-3 rounded-full font-bold transition-all cursor-pointer">
        Save Settings
      </button>
    </form>
  </div>

  <div class="bg-surface-card rounded-2xl border border-deep-border p-6">
    <h3 class="font-headline-h3 text-headline-h3 text-ivory-white mb-6">Working Hours</h3>
    <div class="flex flex-col gap-4">
      {#each ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"] as day}
        <div class="flex items-center justify-between">
          <span class="text-ivory-white text-sm">{day}</span>
          <div class="flex items-center gap-2">
            <select class="bg-surface-charcoal border border-deep-border rounded-xl px-3 py-2 text-sm focus:border-flame-orange focus:ring-0 outline-none text-ivory-white">
              <option>8:00 AM</option>
              <option>9:00 AM</option>
              <option>10:00 AM</option>
            </select>
            <span class="text-muted-gray">to</span>
            <select class="bg-surface-charcoal border border-deep-border rounded-xl px-3 py-2 text-sm focus:border-flame-orange focus:ring-0 outline-none text-ivory-white">
              <option>9:00 PM</option>
              <option>10:00 PM</option>
              <option selected>11:00 PM</option>
            </select>
          </div>
        </div>
      {/each}
    </div>
  </div>
</div>
