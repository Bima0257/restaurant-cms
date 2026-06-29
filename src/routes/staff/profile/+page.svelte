<script lang="ts">
  import { User } from "@lucide/svelte";
  import ProfileSettings from "$lib/components/ui/ProfileSettings.svelte";
</script>

<div class="mb-8">
  <h1 class="font-headline-h1 text-headline-h1 text-ivory-white flex items-center gap-3">
    <User size={28} class="text-flame-orange" />
    Profile
  </h1>
  <p class="text-muted-gray text-body-lg">Manage your account details and security.</p>
</div>

<ProfileSettings />
