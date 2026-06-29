import * as publicEnv from "$env/static/public";
import { auth } from "$lib/stores/auth";

const API_BASE = (publicEnv as Record<string, string>).PUBLIC_API_URL || "http://localhost:8000/api";

const FETCH_TIMEOUT = 15000;

async function fetchWithTimeout(input: RequestInfo | URL, init?: RequestInit): Promise<Response> {
  return fetch(input, { ...init, signal: AbortSignal.timeout(FETCH_TIMEOUT) });
}

let isRefreshing = false;
let refreshQueue: Array<{
  resolve: (token: string) => void;
  reject: (err: any) => void;
}> = [];

async function refreshTokenRequest(): Promise<string | null> {
  const refreshToken = auth.getRefreshToken();
  if (!refreshToken) return null;

  try {
    const res = await fetchWithTimeout(`${API_BASE}/auth/refresh`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ refresh_token: refreshToken }),
    });
    if (!res.ok) return null;
    const data = await res.json();
    localStorage.setItem("token", data.access_token);
    localStorage.setItem("refresh_token", data.refresh_token);
    return data.access_token;
  } catch {
    return null;
  }
}

async function request<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const token = localStorage.getItem("token");
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(options.headers as Record<string, string>),
  };
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  let res = await fetchWithTimeout(`${API_BASE}${endpoint}`, {
    ...options,
    headers,
  });

  if (res.status === 401 && localStorage.getItem("refresh_token")) {
    if (!isRefreshing) {
      isRefreshing = true;
      const newToken = await refreshTokenRequest();
      isRefreshing = false;

      if (newToken) {
        headers["Authorization"] = `Bearer ${newToken}`;
        refreshQueue.forEach((q) => q.resolve(newToken));
        refreshQueue = [];

        res = await fetchWithTimeout(`${API_BASE}${endpoint}`, {
          ...options,
          headers,
        });
      } else {
        refreshQueue.forEach((q) => q.reject(new Error("Refresh failed")));
        refreshQueue = [];
        auth.logout();
        if (typeof window !== "undefined") {
          window.location.href = "/auth/login";
        }
        throw new Error("Session expired. Please log in again.");
      }
    } else {
      return new Promise((resolve, reject) => {
        refreshQueue.push({
          resolve: async (newToken: string) => {
            headers["Authorization"] = `Bearer ${newToken}`;
            try {
              const retryRes = await fetchWithTimeout(`${API_BASE}${endpoint}`, {
                ...options,
                headers,
              });
              if (!retryRes.ok) {
                const errData = await retryRes.json().catch(() => ({ detail: retryRes.statusText }));
                reject(new Error(errData.message || errData.detail || `HTTP ${retryRes.status}`));
                return;
              }
              const data = retryRes.status === 204 ? null : await retryRes.json();
              resolve(data as T);
            } catch (err) {
              reject(err);
            }
          },
          reject,
        });
      });
    }
  }

  if (!res.ok) {
    const error = await res.json().catch(() => ({ message: res.statusText }));
    throw new Error(error.message || error.detail || `HTTP ${res.status}`);
  }

  if (res.status === 204) return null as T;
  return res.json();
}

export const api = {
  // Auth
  login: (email: string, password: string, gRecaptchaResponse?: string) =>
    request<{ access_token: string; refresh_token: string; token_type: string; user: any }>(
      "/auth/login",
      { method: "POST", body: JSON.stringify({ email, password, g_recaptcha_response: gRecaptchaResponse || "" }) }
    ),
  register: (data: { email: string; password: string; full_name: string; phone?: string }) =>
    request<{ message: string; email: string }>(
      "/auth/register",
      { method: "POST", body: JSON.stringify(data) }
    ),
  verifyEmail: (email: string, otp_code: string) =>
    request<{ message: string }>(
      "/auth/verify-email",
      { method: "POST", body: JSON.stringify({ email, otp_code }) }
    ),
  resendOtp: (email: string) =>
    request<{ message: string }>(
      "/auth/resend-otp",
      { method: "POST", body: JSON.stringify({ email }) }
    ),
  refreshToken: (refreshToken: string) =>
    request<{ access_token: string; refresh_token: string; token_type: string }>(
      "/auth/refresh",
      { method: "POST", body: JSON.stringify({ refresh_token: refreshToken }) }
    ),
  logout: (refreshToken: string) =>
    request<{ message: string }>(
      "/auth/logout",
      { method: "POST", body: JSON.stringify({ refresh_token: refreshToken }) }
    ),
  getMe: () => request<any>("/auth/me"),
  updateProfile: (data: any) =>
    request<any>("/auth/profile", { method: "PUT", body: JSON.stringify(data) }),
  changePassword: (oldPassword: string, newPassword: string) =>
    request<{ message: string }>("/auth/change-password", { method: "PUT", body: JSON.stringify({ old_password: oldPassword, new_password: newPassword }) }),

  // Public
  getMenu: (categorySlug?: string) =>
    request<any[]>(`/menu${categorySlug ? `?category_slug=${categorySlug}` : ""}`),
  getMenuItem: (id: number) => request<any>(`/menu/${id}`),
  getCategories: () => request<any[]>("/categories"),

  // Customer
  getCart: () => request<any[]>("/cart"),
  addToCart: (data: { menu_item_id: number; qty: number; notes?: string }) =>
    request<any>("/cart", { method: "POST", body: JSON.stringify(data) }),
  updateCart: (id: number, data: { qty: number }) =>
    request<any>(`/cart/${id}`, { method: "PUT", body: JSON.stringify(data) }),
  deleteCartItem: (id: number) =>
    request<void>(`/cart/${id}`, { method: "DELETE" }),
  createOrder: (data: { payment_method?: string; delivery_address?: string; notes?: string }) =>
    request<any>("/orders", { method: "POST", body: JSON.stringify(data) }),
  getMyOrders: () => request<any[]>("/orders"),
  getMyOrder: (id: number) => request<any>(`/orders/${id}`),
  cancelOrder: (id: number) =>
    request<any>(`/orders/${id}/cancel`, { method: "PUT" }),

  // Staff
  staffGetOrders: (status?: string) =>
    request<any[]>(`/staff/orders${status ? `?status=${status}` : ""}`),
  staffUpdateOrderStatus: (id: number, status: string) =>
    request<any>(`/staff/orders/${id}/status`, {
      method: "PUT",
      body: JSON.stringify({ status }),
    }),
  staffCheckStock: () => request<any[]>("/staff/stock-check"),
  staffGetAlerts: (unresolvedOnly = true) =>
    request<any[]>(`/staff/alerts?unresolved_only=${unresolvedOnly}`),
  staffStockIn: (data: { ingredient_id: number; qty: number; notes?: string }) =>
    request<any>("/staff/stock-in", { method: "POST", body: JSON.stringify(data) }),
  staffAdjustStock: (data: { ingredient_id: number; qty: number; notes?: string }) =>
    request<any>("/staff/stock/adjust", { method: "POST", body: JSON.stringify(data) }),
  staffResolveAlert: (id: number) =>
    request<any>(`/staff/alerts/${id}/resolve`, { method: "PUT" }),

  // Admin
  adminListMenu: (categoryId?: number) =>
    request<any[]>(`/admin/menu${categoryId ? `?category_id=${categoryId}` : ""}`),
  adminGetMenuItem: (id: number) => request<any>(`/admin/menu/${id}`),
  adminCreateMenuItem: (data: any) =>
    request<any>("/admin/menu", { method: "POST", body: JSON.stringify(data) }),
  adminUpdateMenuItem: (id: number, data: any) =>
    request<any>(`/admin/menu/${id}`, { method: "PUT", body: JSON.stringify(data) }),
  adminDeleteMenuItem: (id: number) =>
    request<void>(`/admin/menu/${id}`, { method: "DELETE" }),

  adminListCategories: () => request<any[]>("/admin/categories"),
  adminCreateCategory: (data: any) =>
    request<any>("/admin/categories", { method: "POST", body: JSON.stringify(data) }),
  adminUpdateCategory: (id: number, data: any) =>
    request<any>(`/admin/categories/${id}`, { method: "PUT", body: JSON.stringify(data) }),
  adminDeleteCategory: (id: number) =>
    request<void>(`/admin/categories/${id}`, { method: "DELETE" }),

  adminListIngredients: () => request<any[]>("/admin/inventory/ingredients"),
  adminCreateIngredient: (data: any) =>
    request<any>("/admin/inventory/ingredients", { method: "POST", body: JSON.stringify(data) }),
  adminUpdateIngredient: (id: number, data: any) =>
    request<any>(`/admin/inventory/ingredients/${id}`, { method: "PUT", body: JSON.stringify(data) }),
  adminDeleteIngredient: (id: number) =>
    request<void>(`/admin/inventory/ingredients/${id}`, { method: "DELETE" }),

  adminStockIn: (data: { ingredient_id: number; qty: number; notes?: string }) =>
    request<any>("/admin/inventory/stock-in", { method: "POST", body: JSON.stringify(data) }),
  adminAdjustStock: (data: { ingredient_id: number; qty: number; notes?: string }) =>
    request<any>("/admin/inventory/adjust", { method: "POST", body: JSON.stringify(data) }),
  adminListTransactions: (ingredientId?: number) =>
    request<any[]>(`/admin/inventory/transactions${ingredientId ? `?ingredient_id=${ingredientId}` : ""}`),
  adminListAlerts: (unresolvedOnly = true) =>
    request<any[]>(`/admin/inventory/alerts?unresolved_only=${unresolvedOnly}`),
  adminResolveAlert: (id: number) =>
    request<any>(`/admin/inventory/alerts/${id}/resolve`, { method: "PUT" }),

  adminListSuppliers: () => request<any[]>("/admin/inventory/suppliers"),
  adminCreateSupplier: (data: any) =>
    request<any>("/admin/inventory/suppliers", { method: "POST", body: JSON.stringify(data) }),
  adminUpdateSupplier: (id: number, data: any) =>
    request<any>(`/admin/inventory/suppliers/${id}`, { method: "PUT", body: JSON.stringify(data) }),
  adminDeleteSupplier: (id: number) =>
    request<void>(`/admin/inventory/suppliers/${id}`, { method: "DELETE" }),

  adminListRecipes: (menuItemId: number) =>
    request<any[]>(`/admin/recipes/by-menu/${menuItemId}`),
  adminCreateRecipe: (data: any) =>
    request<any>("/admin/recipes", { method: "POST", body: JSON.stringify(data) }),
  adminDeleteRecipe: (id: number) =>
    request<void>(`/admin/recipes/${id}`, { method: "DELETE" }),
  adminCheckStockForMenu: (menuItemId: number, qty = 1) =>
    request<any>(`/admin/recipes/check-stock/${menuItemId}/${qty}`),

  adminListOrders: (status?: string) =>
    request<any[]>(`/admin/orders${status ? `?status=${status}` : ""}`),
  adminGetOrder: (id: number) => request<any>(`/admin/orders/${id}`),
  adminUpdateOrderStatus: (id: number, status: string) =>
    request<any>(`/admin/orders/${id}/status`, {
      method: "PUT",
      body: JSON.stringify({ status }),
    }),

  // Superadmin
  superadminListAdmins: () => request<any[]>("/superadmin/admins"),
  superadminCreateAdmin: (data: any) =>
    request<any>("/superadmin/admins", { method: "POST", body: JSON.stringify(data) }),
  superadminUpdateAdmin: (id: number, data: any) =>
    request<any>(`/superadmin/admins/${id}`, { method: "PUT", body: JSON.stringify(data) }),
  superadminDeleteAdmin: (id: number) =>
    request<void>(`/superadmin/admins/${id}`, { method: "DELETE" }),

  superadminListStaff: () => request<any[]>("/superadmin/staff"),
  superadminCreateStaff: (data: any) =>
    request<any>("/superadmin/staff", { method: "POST", body: JSON.stringify(data) }),
  superadminUpdateStaff: (id: number, data: any) =>
    request<any>(`/superadmin/staff/${id}`, { method: "PUT", body: JSON.stringify(data) }),
  superadminDeleteStaff: (id: number) =>
    request<void>(`/superadmin/staff/${id}`, { method: "DELETE" }),

  superadminListAccounts: () => request<any[]>("/superadmin/accounts"),

  superadminGetAuditLog: () => request<any[]>("/superadmin/audit-log"),
  superadminResetPassword: (userId: number, newPassword: string) =>
    request<any>(`/superadmin/reset-password/${userId}?new_password=${newPassword}`, {
      method: "PUT",
    }),

  // Reviews
  createReview: (data: { menu_item_id: number; rating: number; comment?: string }) =>
    request<any>("/reviews", { method: "POST", body: JSON.stringify(data) }),
  getMenuReviews: (menuItemId: number) =>
    request<any[]>(`/menu/${menuItemId}/reviews`),
  getMenuRating: (menuItemId: number) =>
    request<{ menu_item_id: number; menu_item_name: string; average_rating: number; total_reviews: number }>(`/menu/${menuItemId}/rating`),
  getMyReviews: () => request<any[]>("/my-reviews"),
  deleteReview: (reviewId: number) =>
    request<any>(`/reviews/${reviewId}`, { method: "DELETE" }),

  health: () => request<{ status: string }>("/health"),

  // Superadmin - Backup
  superadminCreateBackup: () =>
    request<{ message: string; filename: string }>("/superadmin/backup", { method: "POST" }),
  superadminListBackups: () =>
    request<{ filename: string; size: number; created_at: string }[]>("/superadmin/backups"),
  superadminDownloadBackup: async (filename: string): Promise<void> => {
    const token = localStorage.getItem("token");
    const res = await fetchWithTimeout(`${API_BASE}/superadmin/backup/download/${filename}`, {
      headers: token ? { Authorization: `Bearer ${token}` } : {},
    });
    if (!res.ok) throw new Error("Download failed");
    const blob = await res.blob();
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  },
  superadminRestoreBackup: async (file: File): Promise<{ message: string }> => {
    const token = localStorage.getItem("token");
    const formData = new FormData();
    formData.append("file", file);
    const res = await fetchWithTimeout(`${API_BASE}/superadmin/backup/restore`, {
      method: "POST",
      headers: token ? { Authorization: `Bearer ${token}` } : {},
      body: formData,
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ message: res.statusText }));
      throw new Error(err.message || "Restore failed");
    }
    return res.json();
  },
  superadminDeleteBackup: (filename: string) =>
    request<{ message: string }>(`/superadmin/backup/${filename}`, { method: "DELETE" }),

  // Upload
  upload: async (file: File): Promise<{ success: boolean; message: string; data: { url: string } }> => {
    const token = localStorage.getItem("token");
    const formData = new FormData();
    formData.append("file", file);
    const res = await fetchWithTimeout(`${API_BASE}/upload`, {
      method: "POST",
      headers: token ? { Authorization: `Bearer ${token}` } : {},
      body: formData,
    });
    if (!res.ok) {
      const error = await res.json().catch(() => ({ message: res.statusText }));
      throw new Error(error.message || `Upload failed: HTTP ${res.status}`);
    }
    return res.json();
  },

  // Reports
  fetchReportBlob: async (reportType: string, params: Record<string, string> = {}): Promise<Blob> => {
    const token = localStorage.getItem("token");
    const qs = new URLSearchParams(params).toString();
    const res = await fetchWithTimeout(`${API_BASE}/reports/${reportType}${qs ? `?${qs}` : ""}`, {
      headers: token ? { Authorization: `Bearer ${token}` } : {},
    });
    if (!res.ok) {
      const error = await res.json().catch(() => ({ message: res.statusText }));
      throw new Error(error.message || `Download failed: HTTP ${res.status}`);
    }
    return res.blob();
  },
  downloadReport: async (reportType: string, params: Record<string, string> = {}): Promise<void> => {
    const blob = await api.fetchReportBlob(reportType, params);
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${reportType}_report.pdf`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  },
};
