<script lang="ts">
  import { Loader2, Save } from "@lucide/svelte";
  import { toast } from "svelte-sonner";
  import SectionHeading from "$lib/components/ui/SectionHeading.svelte";

  let saving = $state(false);

  let form = $state({
    name: "WorldPlate",
    email: "hello@worldplate.com",
    address: "123 Gourmet Street, Food District, NY 10001",
    phone: "+1 (555) 123-4567",
  });

  const dayNames = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];

  let hours = $state<Record<string, { open: string; close: string }>>(
    Object.fromEntries(dayNames.map((day) => [day, { open: "8:00 AM", close: "11:00 PM" }]))
  );

  async function saveSettings(e: Event) {
    e.preventDefault();
    saving = true;
    try {
      await new Promise((r) => setTimeout(r, 600));
      toast.success("Settings saved successfully");
    } catch (err: any) {
      toast.error(err.message || "Failed to save settings");
    } finally {
      saving = false;
    }
  }
</script>

<div class="mb-8">
  <SectionHeading prefix="Restaurant" highlight="Settings" />
</div>

<div class="max-w-2xl space-y-6">
  <div class="bg-surface-card rounded-2xl border border-deep-border p-6">
    <h3 class="font-headline-h3 text-headline-h3 text-ivory-white mb-6">General Information</h3>
    <form class="flex flex-col gap-4" onsubmit={saveSettings}>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label for="rest-name" class="block text-sm text-muted-gray mb-1">Restaurant Name</label>
          <input id="rest-name"
            class="w-full bg-surface-charcoal border border-deep-border rounded-xl px-4 py-3 text-sm focus:border-flame-orange focus:ring-0 outline-none text-ivory-white"
            type="text"
            bind:value={form.name}
          />
        </div>
        <div>
          <label for="rest-email" class="block text-sm text-muted-gray mb-1">Email</label>
          <input id="rest-email"
            class="w-full bg-surface-charcoal border border-deep-border rounded-xl px-4 py-3 text-sm focus:border-flame-orange focus:ring-0 outline-none text-ivory-white"
            type="email"
            bind:value={form.email}
          />
        </div>
      </div>
      <div>
        <label for="rest-address" class="block text-sm text-muted-gray mb-1">Address</label>
        <input id="rest-address"
          class="w-full bg-surface-charcoal border border-deep-border rounded-xl px-4 py-3 text-sm focus:border-flame-orange focus:ring-0 outline-none text-ivory-white"
          type="text"
          bind:value={form.address}
        />
      </div>
      <div>
        <label for="rest-phone" class="block text-sm text-muted-gray mb-1">Phone</label>
        <input id="rest-phone"
          class="w-full bg-surface-charcoal border border-deep-border rounded-xl px-4 py-3 text-sm focus:border-flame-orange focus:ring-0 outline-none text-ivory-white"
          type="text"
          bind:value={form.phone}
        />
      </div>
      <button type="submit" disabled={saving}
        class="bg-flame-orange hover:bg-flame-hover text-ivory-white py-3 rounded-full font-bold transition-all cursor-pointer disabled:opacity-50 flex items-center justify-center gap-2"
      >
        {#if saving}
          <Loader2 size={16} class="animate-spin" />
          Saving...
        {:else}
          <Save size={16} />
          Save Settings
        {/if}
      </button>
    </form>
  </div>

  <div class="bg-surface-card rounded-2xl border border-deep-border p-6">
    <h3 class="font-headline-h3 text-headline-h3 text-ivory-white mb-6">Working Hours</h3>
    <div class="flex flex-col gap-4">
      {#each dayNames as day}
        <div class="flex items-center justify-between">
          <span class="text-ivory-white text-sm">{day}</span>
          <div class="flex items-center gap-2">
            <select class="bg-surface-charcoal border border-deep-border rounded-xl px-3 py-2 text-sm focus:border-flame-orange focus:ring-0 outline-none text-ivory-white" bind:value={hours[day].open}>
              <option>8:00 AM</option>
              <option>9:00 AM</option>
              <option>10:00 AM</option>
            </select>
            <span class="text-muted-gray">to</span>
            <select class="bg-surface-charcoal border border-deep-border rounded-xl px-3 py-2 text-sm focus:border-flame-orange focus:ring-0 outline-none text-ivory-white" bind:value={hours[day].close}>
              <option>9:00 PM</option>
              <option>10:00 PM</option>
              <option>11:00 PM</option>
            </select>
          </div>
        </div>
      {/each}
    </div>
  </div>
</div>
