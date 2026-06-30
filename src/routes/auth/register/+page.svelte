<script lang="ts">
  import { Eye, EyeOff, UserPlus } from "@lucide/svelte";
  import { goto } from "$app/navigation";
  import { toast } from "svelte-sonner";
  import { api } from "$lib/api";
  import { validatePasswordPolicy } from "$lib/utils/password";

  let fullName = $state("");
  let email = $state("");
  let phone = $state("");
  let password = $state("");
  let confirmPassword = $state("");
  let showPassword = $state(false);
  let showConfirm = $state(false);
  let loading = $state(false);
  let passwordErrors = $state<string[]>([]);

  function onPasswordInput() {
    if (password) {
      passwordErrors = validatePasswordPolicy(password, email);
    } else {
      passwordErrors = [];
    }
  }

  async function handleSubmit(e: Event) {
    e.preventDefault();
    if (password !== confirmPassword) {
      toast.error("Passwords do not match");
      return;
    }
    const policyErrors = validatePasswordPolicy(password, email);
    if (policyErrors.length > 0) {
      toast.error("Password does not meet requirements: " + policyErrors.join(", "));
      return;
    }
    loading = true;
    try {
      const res = await api.register({
        email,
        password,
        full_name: fullName,
        phone: phone || undefined,
      });
      goto(`/auth/verify-email?email=${encodeURIComponent(res.email)}`);
    } catch (err: any) {
      toast.error(err.message);
    } finally {
      loading = false;
    }
  }
</script>

<div class="min-h-screen flex items-center justify-center px-gutter pt-32 pb-20">
  <div class="bg-surface-card rounded-3xl p-8 md:p-12 w-full max-w-md">
    <div class="text-center mb-8">
      <div class="font-headline-h2 text-headline-h2 text-flame-orange font-extrabold mb-2">WorldPlate</div>
      <h1 class="font-headline-h3 text-headline-h3 text-ivory-white">Create Account</h1>
      <p class="text-muted-gray text-sm mt-2">Join us for an amazing culinary experience</p>
    </div>
    <form class="flex flex-col gap-4" onsubmit={handleSubmit}>
      <div class="grid grid-cols-1 gap-4">
        <input
          class="bg-surface-charcoal border border-deep-border rounded-xl px-4 py-3 text-sm focus:border-flame-orange focus:ring-0 outline-none text-ivory-white"
          placeholder="Full Name"
          type="text"
          bind:value={fullName}
          required
        />
      </div>
      <input
        class="bg-surface-charcoal border border-deep-border rounded-xl px-4 py-3 text-sm focus:border-flame-orange focus:ring-0 outline-none text-ivory-white"
        placeholder="Email Address"
        type="email"
        bind:value={email}
        required
      />
      <input
        class="bg-surface-charcoal border border-deep-border rounded-xl px-4 py-3 text-sm focus:border-flame-orange focus:ring-0 outline-none text-ivory-white"
        placeholder="Phone (optional)"
        type="tel"
        bind:value={phone}
      />
      <div>
        <div class="relative">
          <input
            class="bg-surface-charcoal border border-deep-border rounded-xl px-4 py-3 pr-10 text-sm focus:border-flame-orange focus:ring-0 outline-none text-ivory-white w-full"
            placeholder="Password"
            type={showPassword ? "text" : "password"}
            bind:value={password}
            oninput={onPasswordInput}
            required
          />
          <button type="button" onclick={() => showPassword = !showPassword} class="absolute right-3 top-1/2 -translate-y-1/2 text-muted-gray hover:text-ivory-white cursor-pointer">
            {#if showPassword}
              <EyeOff size={18} />
            {:else}
              <Eye size={18} />
            {/if}
          </button>
        </div>
        {#if passwordErrors.length > 0}
          <ul class="mt-1 space-y-0.5">
            {#each passwordErrors as err}
              <li class="text-red-400 text-xs">- {err}</li>
            {/each}
          </ul>
        {:else if password.length >= 8}
          <p class="text-green-400 text-xs mt-1">Password looks good</p>
        {/if}
      </div>
      <div class="relative">
        <input
          class="bg-surface-charcoal border border-deep-border rounded-xl px-4 py-3 pr-10 text-sm focus:border-flame-orange focus:ring-0 outline-none text-ivory-white w-full"
          placeholder="Confirm Password"
          type={showConfirm ? "text" : "password"}
          bind:value={confirmPassword}
          required
        />
        <button type="button" onclick={() => showConfirm = !showConfirm} class="absolute right-3 top-1/2 -translate-y-1/2 text-muted-gray hover:text-ivory-white cursor-pointer">
          {#if showConfirm}
            <EyeOff size={18} />
          {:else}
            <Eye size={18} />
          {/if}
        </button>
      </div>
      <button disabled={loading} class="bg-flame-orange hover:bg-flame-hover text-ivory-white py-3 rounded-full font-bold transition-all flex items-center justify-center gap-2 cursor-pointer mt-2 disabled:opacity-50">
        <UserPlus size={18} />
        {loading ? "Creating Account..." : "Create Account"}
      </button>
    </form>
    <p class="text-center text-muted-gray text-sm mt-6">
      Already have an account? <a href="/auth/login" class="text-flame-orange hover:underline">Sign In</a>
    </p>
  </div>
</div>
