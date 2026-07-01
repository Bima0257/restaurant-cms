import { browser } from "$app/environment";
import { redirect } from "@sveltejs/kit";
import { auth } from "$lib/stores/auth";
import { get } from "svelte/store";

type Role = "superadmin" | "admin" | "staff" | "customer";

export function requireAuth(roles?: Role[]) {
  if (!browser) return;

  const user = get(auth);
  if (!user) {
    throw redirect(302, "/auth/login");
  }

  if (roles && !roles.includes(user.role)) {
    if (user.role === "customer") throw redirect(302, "/dashboard");
    if (user.role === "superadmin") throw redirect(302, "/superadmin/accounts");
    if (user.role === "admin") throw redirect(302, "/admin");
    if (user.role === "staff") throw redirect(302, "/staff/orders");
    throw redirect(302, "/");
  }
}

export function redirectAuthenticated() {
  if (!browser) return;

  const user = get(auth);
  if (!user) return;

  if (user.role === "superadmin") throw redirect(302, "/superadmin/accounts");
  if (user.role === "admin") throw redirect(302, "/admin");
  if (user.role === "staff") throw redirect(302, "/staff/orders");
  if (user.role === "customer") throw redirect(302, "/dashboard");
}
