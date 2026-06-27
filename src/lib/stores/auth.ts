import { writable } from "svelte/store";

export interface User {
  id: number;
  email: string;
  full_name: string;
  phone: string | null;
  avatar_url: string | null;
  role: "superadmin" | "admin" | "staff" | "customer";
  is_active: boolean;
  created_at: string;
}

function createAuthStore() {
  const stored = typeof localStorage !== "undefined"
    ? localStorage.getItem("user")
    : null;
  const initial = stored ? JSON.parse(stored) : null;

  const { subscribe, set, update } = writable<User | null>(initial);

  return {
    subscribe,
    getToken: (): string | null =>
      typeof localStorage !== "undefined" ? localStorage.getItem("token") : null,
    getRefreshToken: (): string | null =>
      typeof localStorage !== "undefined" ? localStorage.getItem("refresh_token") : null,
    getLastActive: (): number => {
      if (typeof localStorage === "undefined") return Date.now();
      const val = localStorage.getItem("last_active");
      return val ? parseInt(val, 10) : Date.now();
    },
    updateLastActive: () => {
      if (typeof localStorage !== "undefined") {
        localStorage.setItem("last_active", String(Date.now()));
      }
    },
    login: (user: User, token: string, refreshToken: string) => {
      localStorage.setItem("token", token);
      localStorage.setItem("refresh_token", refreshToken);
      localStorage.setItem("user", JSON.stringify(user));
      localStorage.setItem("last_active", String(Date.now()));
      set(user);
    },
    logout: () => {
      localStorage.removeItem("token");
      localStorage.removeItem("refresh_token");
      localStorage.removeItem("user");
      localStorage.removeItem("last_active");
      set(null);
    },
    updateUser: (user: User) => {
      localStorage.setItem("user", JSON.stringify(user));
      set(user);
    },
    set,
  };
}

export const auth = createAuthStore();
