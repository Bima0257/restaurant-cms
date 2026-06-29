<script lang="ts">
  import { onMount } from "svelte";
  import { goto } from "$app/navigation";
  import { User, Mail, Phone, Lock, Save } from "@lucide/svelte";
  import { toast } from "svelte-sonner";
  import { api } from "$lib/api";
  import { auth } from "$lib/stores/auth";
  import { get } from "svelte/store";

  let user = $derived(get(auth));

  let fullName = $state("");
  let email = $state("");
  let phone = $state("");
  let saving = $state(false);

  let currentPassword = $state("");
  let newPassword = $state("");
  let confirmPassword = $state("");
  let changingPassword = $state(false);

  onMount(async () => {
    if (!get(auth)) {
      goto("/auth/login");
      return;
    }
    fullName = user?.full_name || "";
    email = user?.email || "";
    phone = user?.phone || "";
  });

  async function saveProfile() {
    saving = true;
    try {
      const updated = await api.updateProfile({ full_name: fullName, phone });
      auth.updateUser(updated);
      toast.success("Profile updated");
    } catch (err: any) {
      toast.error(err.message || "Failed to update profile");
    } finally {
      saving = false;
    }
  }

  async function changePassword() {
    if (newPassword !== confirmPassword) {
      toast.error("Passwords do not match");
      return;
    }
    if (newPassword.length < 6) {
      toast.error("Password must be at least 6 characters");
      return;
    }
    changingPassword = true;
    try {
      await api.changePassword(currentPassword, newPassword);
      toast.success("Password changed");
      currentPassword = "";
      newPassword = "";
      confirmPassword = "";
    } catch (err: any) {
      toast.error(err.message || "Failed to change password");
    } finally {
      changingPassword = false;
    }
  }
</script>

<div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
  <div class="bg-surface-card rounded-[1.5rem] border border-deep-border p-6">
    <h3 class="font-headline-h3 text-headline-h3 text-ivory-white mb-6">Personal Information</h3>
    <div class="space-y-4">
      <div>
        <label class="text-sm text-muted-gray block mb-1">Full Name</label>
        <div class="relative">
          <User size={16} class="absolute left-4 top-1/2 -translate-y-1/2 text-muted-gray" />
          <input
            type="text"
            bind:value={fullName}
            class="w-full bg-surface-charcoal border border-deep-border rounded-xl pl-11 pr-4 py-3 text-sm text-ivory-white placeholder:text-muted-gray focus:border-flame-orange focus:ring-0 outline-none"
          />
        </div>
      </div>
      <div>
        <label class="text-sm text-muted-gray block mb-1">Email</label>
        <div class="relative">
          <Mail size={16} class="absolute left-4 top-1/2 -translate-y-1/2 text-muted-gray" />
          <input
            type="email"
            bind:value={email}
            disabled
            class="w-full bg-surface-charcoal border border-deep-border rounded-xl pl-11 pr-4 py-3 text-sm text-muted-gray focus:border-flame-orange focus:ring-0 outline-none cursor-not-allowed"
          />
        </div>
        <p class="text-xs text-muted-gray mt-1">Email cannot be changed.</p>
      </div>
      <div>
        <label class="text-sm text-muted-gray block mb-1">Phone</label>
        <div class="relative">
          <Phone size={16} class="absolute left-4 top-1/2 -translate-y-1/2 text-muted-gray" />
          <input
            type="tel"
            bind:value={phone}
            class="w-full bg-surface-charcoal border border-deep-border rounded-xl pl-11 pr-4 py-3 text-sm text-ivory-white placeholder:text-muted-gray focus:border-flame-orange focus:ring-0 outline-none"
          />
        </div>
      </div>
      <button
        onclick={saveProfile}
        disabled={saving}
        class="w-full bg-flame-orange hover:bg-flame-hover text-ivory-white py-3 rounded-xl font-bold text-sm transition-all flex items-center justify-center gap-2 cursor-pointer disabled:opacity-50"
      >
        <Save size={16} />
        {saving ? "Saving..." : "Save Changes"}
      </button>
    </div>
  </div>

  <div class="bg-surface-card rounded-[1.5rem] border border-deep-border p-6">
    <h3 class="font-headline-h3 text-headline-h3 text-ivory-white mb-6">Change Password</h3>
    <div class="space-y-4">
      <div>
        <label class="text-sm text-muted-gray block mb-1">Current Password</label>
        <div class="relative">
          <Lock size={16} class="absolute left-4 top-1/2 -translate-y-1/2 text-muted-gray" />
          <input
            type="password"
            bind:value={currentPassword}
            class="w-full bg-surface-charcoal border border-deep-border rounded-xl pl-11 pr-4 py-3 text-sm text-ivory-white placeholder:text-muted-gray focus:border-flame-orange focus:ring-0 outline-none"
          />
        </div>
      </div>
      <div>
        <label class="text-sm text-muted-gray block mb-1">New Password</label>
        <div class="relative">
          <Lock size={16} class="absolute left-4 top-1/2 -translate-y-1/2 text-muted-gray" />
          <input
            type="password"
            bind:value={newPassword}
            class="w-full bg-surface-charcoal border border-deep-border rounded-xl pl-11 pr-4 py-3 text-sm text-ivory-white placeholder:text-muted-gray focus:border-flame-orange focus:ring-0 outline-none"
          />
        </div>
      </div>
      <div>
        <label class="text-sm text-muted-gray block mb-1">Confirm New Password</label>
        <div class="relative">
          <Lock size={16} class="absolute left-4 top-1/2 -translate-y-1/2 text-muted-gray" />
          <input
            type="password"
            bind:value={confirmPassword}
            class="w-full bg-surface-charcoal border border-deep-border rounded-xl pl-11 pr-4 py-3 text-sm text-ivory-white placeholder:text-muted-gray focus:border-flame-orange focus:ring-0 outline-none"
          />
        </div>
      </div>
      <button
        onclick={changePassword}
        disabled={changingPassword || !currentPassword || !newPassword || !confirmPassword}
        class="w-full bg-surface-charcoal border border-deep-border hover:border-flame-orange text-ivory-white py-3 rounded-xl font-bold text-sm transition-all cursor-pointer disabled:opacity-50"
      >
        <div class="flex items-center justify-center gap-2">
          <Lock size={16} />
          {changingPassword ? "Changing..." : "Change Password"}
        </div>
      </button>
    </div>
  </div>
</div>
