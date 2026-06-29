<script lang="ts">
  import { onMount, onDestroy } from "svelte";
  import { goto } from "$app/navigation";
  import { browser } from "$app/environment";
  import "./layout.css";
  import { api } from "$lib/api";
  import { auth } from "$lib/stores/auth";
  import { get } from "svelte/store";
  import { Toaster } from "svelte-sonner";
  import ConfirmDialog from "$lib/components/ui/ConfirmDialog.svelte";

  let { children } = $props();

  const IDLE_TIMEOUT_MS = 30 * 60 * 1000;
  const CHECK_INTERVAL_MS = 30 * 1000;
  let idleTimer: ReturnType<typeof setInterval> | null = null;

  const activityEvents = ["mousemove", "mousedown", "keydown", "click", "scroll", "touchstart", "wheel"];

  function onUserActivity() {
    auth.updateLastActive();
  }

  function checkIdleTimeout() {
    if (!browser) return;
    const user = get(auth);
    if (!user) return;

    const lastActive = auth.getLastActive();
    const elapsed = Date.now() - lastActive;
    if (elapsed >= IDLE_TIMEOUT_MS) {
      const refreshToken = auth.getRefreshToken();
      if (refreshToken) {
        try { api.logout(refreshToken); } catch { /* ignore */ }
      }
      auth.logout();
      goto("/auth/login");
    }
  }

  onMount(() => {
    if (!browser) return;

    auth.updateLastActive();

    activityEvents.forEach((event) =>
      window.addEventListener(event, onUserActivity, { passive: true })
    );

    idleTimer = setInterval(checkIdleTimeout, CHECK_INTERVAL_MS);
  });

  onDestroy(() => {
    if (!browser) return;

    activityEvents.forEach((event) =>
      window.removeEventListener(event, onUserActivity)
    );
    if (idleTimer) clearInterval(idleTimer);
  });
</script>

<Toaster theme="dark" position="top-right" richColors closeButton />
<ConfirmDialog />
{@render children()}
