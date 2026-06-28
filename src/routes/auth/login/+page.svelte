<script lang="ts">
  import { Eye, EyeOff, LogIn } from "@lucide/svelte";
  import { goto } from "$app/navigation";
  import { page } from "$app/stores";
  import { onMount } from "svelte";
  import * as publicEnv from "$env/static/public";

  let PUBLIC_RECAPTCHA_SITE_KEY = $derived((publicEnv as Record<string, string>).PUBLIC_RECAPTCHA_SITE_KEY || "");
  import { toast } from "svelte-sonner";
  import { api } from "$lib/api";
  import { auth } from "$lib/stores/auth";

  let email = $state("");
  let password = $state("");
  let showPassword = $state(false);
  let loading = $state(false);
  let recaptchaToken = $state("");
  let recaptchaWidgetId: string | null = null;
  let recaptchaReady = $state(false);

  function renderReCaptcha() {
    if (!(window as any).grecaptcha || !PUBLIC_RECAPTCHA_SITE_KEY) {
      recaptchaReady = true;
      return;
    }
    const container = document.getElementById("g-recaptcha");
    if (!container) return;
    container.innerHTML = "";
    recaptchaWidgetId = (window as any).grecaptcha.render(container, {
      sitekey: PUBLIC_RECAPTCHA_SITE_KEY,
      theme: "dark",
      callback: (token: string) => { recaptchaToken = token; },
      "expired-callback": () => { recaptchaToken = ""; },
    });
    recaptchaReady = true;
  }

  function resetReCaptcha() {
    recaptchaToken = "";
    if (recaptchaWidgetId && (window as any).grecaptcha) {
      (window as any).grecaptcha.reset(recaptchaWidgetId);
    }
  }

  onMount(() => {
    if ($page.url.searchParams.get("verified") === "1") {
      toast.success("Email verified successfully! You can now log in.");
    }
    if (PUBLIC_RECAPTCHA_SITE_KEY) {
      const script = document.createElement("script");
      script.src = "https://www.google.com/recaptcha/api.js?render=explicit&onload=recaptchaOnLoad";
      script.async = true;
      script.defer = true;
      (window as any).recaptchaOnLoad = renderReCaptcha;
      document.head.appendChild(script);
    } else {
      recaptchaReady = true;
    }
  });

  async function handleSubmit(e: Event) {
    e.preventDefault();

    if (PUBLIC_RECAPTCHA_SITE_KEY && !recaptchaToken) {
      toast.error("Please complete the reCAPTCHA verification.");
      return;
    }

    loading = true;
    try {
      const res = await api.login(email, password, recaptchaToken);
      auth.login(res.user, res.access_token, res.refresh_token);
      const role = res.user.role;
      if (role === "superadmin") goto("/superadmin");
      else if (role === "admin") goto("/admin");
      else if (role === "staff") goto("/staff/orders");
      else goto("/");
    } catch (err: any) {
      if (err.message.includes("Email not verified")) {
        toast.error("Email not verified. Please verify your email first.");
      } else {
        toast.error(err.message);
      }
      resetReCaptcha();
    } finally {
      loading = false;
    }
  }
</script>

<div class="min-h-screen flex items-center justify-center px-gutter pt-32 pb-20">
  <div class="bg-surface-card rounded-3xl p-8 md:p-12 w-full max-w-md">
    <div class="text-center mb-8">
      <div class="font-headline-h2 text-headline-h2 text-flame-orange font-extrabold mb-2">WorldPlate</div>
      <h1 class="font-headline-h3 text-headline-h3 text-ivory-white">Welcome Back</h1>
      <p class="text-muted-gray text-sm mt-2">Sign in to your account</p>
    </div>
    <form class="flex flex-col gap-4" onsubmit={handleSubmit}>
      <input
        class="bg-surface-charcoal border border-deep-border rounded-xl px-4 py-3 text-sm focus:border-flame-orange focus:ring-0 outline-none text-ivory-white"
        placeholder="Email Address"
        type="email"
        bind:value={email}
        required
      />
      <div class="relative">
        <input
          class="bg-surface-charcoal border border-deep-border rounded-xl px-4 py-3 pr-10 text-sm focus:border-flame-orange focus:ring-0 outline-none text-ivory-white w-full"
          placeholder="Password"
          type={showPassword ? "text" : "password"}
          bind:value={password}
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

      {#if PUBLIC_RECAPTCHA_SITE_KEY}
        <div class="flex flex-col gap-2">
          <span class="text-muted-gray text-xs font-medium">Verification</span>
          <div class="bg-surface-charcoal border border-deep-border rounded-xl overflow-hidden">
            <div class="flex justify-center py-3 sm:py-4">
              <div id="g-recaptcha" class="max-sm:scale-[0.77] max-sm:origin-center"></div>
            </div>
          </div>
        </div>
      {/if}

      <button disabled={loading || (Boolean(PUBLIC_RECAPTCHA_SITE_KEY) && (!recaptchaReady || !recaptchaToken))} class="bg-flame-orange hover:bg-flame-hover text-ivory-white py-3 rounded-full font-bold transition-all flex items-center justify-center gap-2 cursor-pointer mt-2 disabled:opacity-50">
        <LogIn size={18} />
        {loading ? "Signing In..." : "Sign In"}
      </button>
    </form>
    <p class="text-center text-muted-gray text-sm mt-6">
      Don't have an account? <a href="/auth/register" class="text-flame-orange hover:underline">Register</a>
    </p>
  </div>
</div>
