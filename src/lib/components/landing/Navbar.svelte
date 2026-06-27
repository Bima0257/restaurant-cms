<script lang="ts">
  import { Menu, X, User, LogOut } from "@lucide/svelte";
  import { page } from "$app/stores";
  import { auth } from "$lib/stores/auth";
  import { get } from "svelte/store";

  let mobileOpen = $state(false);

  import { api } from "$lib/api";

  const navLinks = [
    { label: "Home", href: "/" },
    { label: "Menu", href: "/menu" },
    { label: "About Us", href: "/about" },
    { label: "Contact", href: "/contact" },
  ];

  let user = $derived(get(auth));

  async function handleLogout() {
    const refreshToken = auth.getRefreshToken();
    if (refreshToken) {
      try { await api.logout(refreshToken); } catch { /* ignore */ }
    }
    auth.logout();
  }

  function getDashboardLink() {
    if (!user) return "/auth/login";
    if (user.role === "superadmin") return "/superadmin/admins";
    if (user.role === "admin") return "/admin";
    if (user.role === "staff") return "/staff/orders";
    return "/dashboard";
  }
</script>

<nav class="fixed top-0 w-full z-50 bg-surface/80 backdrop-blur-md shadow-sm">
  <div class="flex justify-between items-center px-gutter py-4 max-w-grid-max-width mx-auto">
    <a href="/" class="font-headline-h3 text-headline-h3 font-extrabold text-flame-orange">
      WorldPlate
    </a>

    <div class="hidden md:flex gap-8 items-center">
      {#each navLinks as link}
        <a
          href={link.href}
          class={link.href === $page.url.pathname || ($page.url.pathname === "/" && link.href === "/")
            ? "bg-flame-orange rounded-full px-4 py-1 font-bold text-ivory-white"
            : "text-ivory-white font-medium hover:text-flame-orange transition-colors duration-300"}
        >
          {link.label}
        </a>
      {/each}
    </div>

    <div class="flex items-center gap-4">
      {#if user}
        <a href={getDashboardLink()} class="flex items-center gap-2 text-flame-orange font-bold hover:opacity-80 transition-opacity">
          <User size={18} />
          <span class="hidden md:inline">{user.full_name}</span>
        </a>
        <button onclick={handleLogout} class="text-muted-gray hover:text-red-400 transition-colors cursor-pointer" aria-label="Logout">
          <LogOut size={18} class="hidden md:block" />
        </button>
      {:else}
        <a href="/auth/login" class="text-ivory-white font-medium hover:text-flame-orange transition-colors duration-300 hidden md:inline">
          Sign In
        </a>
        <a
          href="/auth/register"
          class="bg-flame-orange hover:bg-flame-hover text-ivory-white px-5 py-2 rounded-full font-bold text-sm transition-all"
        >
          Register
        </a>
      {/if}

      <button class="md:hidden text-ivory-white" onclick={() => (mobileOpen = !mobileOpen)} aria-label="Toggle menu">
        {#if mobileOpen}
          <X size={24} />
        {:else}
          <Menu size={24} />
        {/if}
      </button>
    </div>
  </div>

  {#if mobileOpen}
    <div class="md:hidden bg-surface/95 backdrop-blur-md border-t border-deep-border px-gutter py-4">
      {#each navLinks as link}
        <a
          href={link.href}
          class="block py-3 text-ivory-white font-medium hover:text-flame-orange transition-colors"
          onclick={() => (mobileOpen = false)}
        >
          {link.label}
        </a>
      {/each}
      <div class="border-t border-deep-border mt-4 pt-4 flex flex-col gap-3">
        {#if user}
          <a href={getDashboardLink()} class="text-flame-orange font-bold">Dashboard</a>
          <button onclick={() => { handleLogout(); mobileOpen = false; }} class="text-left text-red-400 font-medium cursor-pointer">Logout</button>
        {:else}
          <a href="/auth/login" class="text-ivory-white font-medium">Sign In</a>
          <a href="/auth/register" class="text-flame-orange font-bold">Register</a>
        {/if}
      </div>
    </div>
  {/if}
</nav>
