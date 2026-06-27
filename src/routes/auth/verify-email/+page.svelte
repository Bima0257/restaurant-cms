<script lang="ts">
  import { MailCheck, ArrowLeft, Loader2, Timer, AlertTriangle } from "@lucide/svelte";
  import { goto } from "$app/navigation";
  import { page } from "$app/stores";
  import { onMount, onDestroy } from "svelte";
  import { toast } from "svelte-sonner";
  import { api } from "$lib/api";

  const OTP_EXPIRE_SECONDS = 120;

  let email = $state($page.url.searchParams.get("email") || "");
  let otpCode = $state("");
  let loading = $state(false);
  let resendLoading = $state(false);
  let resendCooldown = $state(0);
  let countdownInterval: ReturnType<typeof setInterval> | null = null;

  let expiryTimer = $state(OTP_EXPIRE_SECONDS);
  let otpExpired = $state(false);
  let expiryInterval: ReturnType<typeof setInterval> | null = null;

  function formatTime(seconds: number): string {
    const m = Math.floor(seconds / 60);
    const s = seconds % 60;
    return `${m}:${s.toString().padStart(2, "0")}`;
  }

  function startExpiryCountdown(seconds: number) {
    otpExpired = false;
    expiryTimer = seconds;
    if (expiryInterval) clearInterval(expiryInterval);
    expiryInterval = setInterval(() => {
      expiryTimer -= 1;
      if (expiryTimer <= 0) {
        expiryTimer = 0;
        otpExpired = true;
        if (expiryInterval) clearInterval(expiryInterval);
      }
    }, 1000);
  }

  function startCountdown(seconds: number) {
    resendCooldown = seconds;
    if (countdownInterval) clearInterval(countdownInterval);
    countdownInterval = setInterval(() => {
      resendCooldown -= 1;
      if (resendCooldown <= 0) {
        resendCooldown = 0;
        if (countdownInterval) clearInterval(countdownInterval);
      }
    }, 1000);
  }

  onMount(() => {
    if (email) {
      startExpiryCountdown(OTP_EXPIRE_SECONDS);
    }
  });

  onDestroy(() => {
    if (expiryInterval) clearInterval(expiryInterval);
    if (countdownInterval) clearInterval(countdownInterval);
  });

  async function handleVerify(e: Event) {
    e.preventDefault();
    if (!email) {
      toast.error("Email is required");
      return;
    }
    if (otpCode.length !== 6) {
      toast.error("Please enter the 6-digit OTP code");
      return;
    }
    loading = true;
    try {
      await api.verifyEmail(email, otpCode);
      goto("/auth/login?verified=1");
    } catch (err: any) {
      toast.error(err.message);
    } finally {
      loading = false;
    }
  }

  async function handleResend() {
    if (!email || resendCooldown > 0) return;
    resendLoading = true;
    try {
      const res = await api.resendOtp(email);
      toast.success(res.message);
      startCountdown(60);
      startExpiryCountdown(OTP_EXPIRE_SECONDS);
    } catch (err: any) {
      toast.error(err.message);
    } finally {
      resendLoading = false;
    }
  }
</script>

<div class="min-h-screen flex items-center justify-center px-gutter pt-32 pb-20">
  <div class="bg-surface-card rounded-3xl p-8 md:p-12 w-full max-w-md">
    <div class="text-center mb-8">
      <div class="flex justify-center mb-4">
        <div class="bg-flame-orange/10 p-4 rounded-full">
          <MailCheck class="text-flame-orange" size={36} />
        </div>
      </div>
      <h1 class="font-headline-h3 text-headline-h3 text-ivory-white">Verify Your Email</h1>
      <p class="text-muted-gray text-sm mt-2">Enter the 6-digit code sent to your email</p>
    </div>

    <form class="flex flex-col gap-4" onsubmit={handleVerify}>
      <input
        class="bg-surface-charcoal border border-deep-border rounded-xl px-4 py-3 text-sm focus:border-flame-orange focus:ring-0 outline-none text-ivory-white"
        placeholder="Email Address"
        type="email"
        bind:value={email}
        required
      />

      <div>
        <input
          class="bg-surface-charcoal border border-deep-border rounded-xl px-4 py-3 text-sm focus:border-flame-orange focus:ring-0 outline-none text-ivory-white w-full text-center text-2xl tracking-[8px]"
          placeholder="000000"
          type="text"
          inputmode="numeric"
          maxlength={6}
          bind:value={otpCode}
          required
        />
        <p class="text-muted-gray text-xs mt-1 text-center">6-digit OTP code</p>
      </div>

      {#if otpExpired}
        <div class="flex items-center justify-center gap-2 text-red-400 text-sm">
          <AlertTriangle size={16} />
          <span>OTP has expired. Please resend a new code.</span>
        </div>
      {:else if expiryTimer > 0}
        <div class="flex items-center justify-center gap-2 text-flame-orange text-sm">
          <Timer size={16} />
          <span>OTP expires in <strong>{formatTime(expiryTimer)}</strong></span>
        </div>
      {/if}

      <button disabled={loading || otpExpired} class="bg-flame-orange hover:bg-flame-hover text-ivory-white py-3 rounded-full font-bold transition-all flex items-center justify-center gap-2 cursor-pointer mt-2 disabled:opacity-50">
        {#if loading}
          <Loader2 size={18} class="animate-spin" />
          Verifying...
        {:else}
          Verify Email
        {/if}
      </button>
    </form>

    <div class="text-center mt-6 space-y-3">
      <button
        onclick={handleResend}
        disabled={resendLoading || resendCooldown > 0 || !email}
        class="text-sm text-flame-orange hover:underline cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {#if resendCooldown > 0}
          Resend code in {resendCooldown}s
        {:else if resendLoading}
          Sending...
        {:else}
          Resend OTP Code
        {/if}
      </button>

      <div>
        <a href="/auth/login" class="text-muted-gray text-sm hover:text-ivory-white transition-colors inline-flex items-center gap-1">
          <ArrowLeft size={14} />
          Back to Login
        </a>
      </div>
    </div>
  </div>
</div>
