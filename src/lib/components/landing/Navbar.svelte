<script lang="ts">
  import { House, UtensilsCrossed, Info, Phone, User, LogIn, LogOut } from "@lucide/svelte";
  import { page } from "$app/stores";
  import { auth } from "$lib/stores/auth";
  import { get } from "svelte/store";
  import { api } from "$lib/api";

  const navLinks = [
    { label: "Home", href: "/", icon: House },
    { label: "Menu", href: "/menu", icon: UtensilsCrossed },
    { label: "About Us", href: "/about", icon: Info },
    { label: "Contact", href: "/contact", icon: Phone },
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
        <a href="/auth/login" class="text-ivory-white font-medium hover:text-flame-orange transition-colors duration-300">
          Sign In
        </a>
        <a
          href="/auth/register"
          class="hidden md:inline bg-flame-orange hover:bg-flame-hover text-ivory-white px-5 py-2 rounded-full font-bold text-sm transition-all"
        >
          Register
        </a>
      {/if}
    </div>
  </div>
</nav>

<div class="md:hidden fixed bottom-0 left-0 w-full bg-surface-container-lowest/80 backdrop-blur-lg border-t border-deep-border flex justify-around items-center py-3 px-2 z-50">
  {#each navLinks as link}
    <a
      href={link.href}
      class={"flex flex-col items-center gap-1 " + (($page.url.pathname === link.href) || ($page.url.pathname === "/" && link.href === "/") ? "text-flame-orange" : "text-muted-gray")}
    >
      <link.icon size={20} />
      <span class="text-[10px] font-bold">{link.label}</span>
    </a>
  {/each}
  {#if user}
    <a
      href={getDashboardLink()}
      class={"flex flex-col items-center gap-1 " + ($page.url.pathname.startsWith("/dashboard") || $page.url.pathname.startsWith("/admin") || $page.url.pathname.startsWith("/staff") || $page.url.pathname.startsWith("/superadmin") ? "text-flame-orange" : "text-muted-gray")}
    >
      <User size={20} />
      <span class="text-[10px] font-bold">Profile</span>
    </a>
  {:else}
    <a
      href="/auth/login"
      class={"flex flex-col items-center gap-1 " + ($page.url.pathname.startsWith("/auth") ? "text-flame-orange" : "text-muted-gray")}
    >
      <LogIn size={20} />
      <span class="text-[10px] font-bold">Sign In</span>
    </a>
  {/if}
</div>

