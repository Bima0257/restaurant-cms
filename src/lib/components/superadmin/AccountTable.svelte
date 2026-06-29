<script lang="ts">
  import { onMount } from "svelte";
  import { Plus, Search, Pencil, Trash2, KeyRound, X, Loader2 } from "@lucide/svelte";
  import { toast } from "svelte-sonner";
  import { confirmAction } from "$lib/utils/confirm";

  let {
    apiList,
    onCreate,
    onUpdate,
    onDelete,
    onResetPassword,
  }: {
    apiList: () => Promise<any[]>;
    onCreate: (data: any) => Promise<any>;
    onUpdate: (id: number, data: any, role: string) => Promise<any>;
    onDelete: (id: number, role: string) => Promise<void>;
    onResetPassword: (id: number, password: string) => Promise<any>;
  } = $props();

  let accounts = $state<any[]>([]);
  let loading = $state(true);
  let searchQuery = $state("");
  let roleFilter = $state<"all" | "admin" | "staff">("all");
  let showModal = $state(false);
  let editing = $state<any>(null);
  let showPasswordModal = $state(false);
  let passwordTarget = $state<any>(null);
  let newPassword = $state("");
  let saving = $state(false);

  let form = $state({ email: "", password: "", full_name: "", phone: "", role: "admin" });

  let filtered = $derived(
    accounts.filter((a) => {
      const matchesSearch =
        a.full_name?.toLowerCase().includes(searchQuery.toLowerCase()) ||
        a.email?.toLowerCase().includes(searchQuery.toLowerCase());
      const matchesRole = roleFilter === "all" || a.role === roleFilter;
      return matchesSearch && matchesRole;
    })
  );

  let counts = $derived({
    all: accounts.length,
    admin: accounts.filter((a) => a.role === "admin").length,
    staff: accounts.filter((a) => a.role === "staff").length,
  });

  async function load() {
    loading = true;
    try {
      accounts = await apiList();
    } catch (err: any) {
      toast.error(err.message || "Failed to load accounts");
    } finally {
      loading = false;
    }
  }

  function getInitials(name: string) {
    return (
      name
        ?.split(" ")
        .map((n) => n[0])
        .join("")
        .toUpperCase()
        .slice(0, 2) || "?"
    );
  }

  const statusColors: Record<string, string> = {
    true: "bg-green-500/10 text-green-400 border-green-500/20",
    false: "bg-red-500/10 text-red-400 border-red-500/20",
  };

  const statusLabels: Record<string, string> = {
    true: "Active",
    false: "Inactive",
  };

  const roleColors: Record<string, string> = {
    admin: "bg-purple-500/10 text-purple-400 border-purple-500/20",
    staff: "bg-blue-500/10 text-blue-400 border-blue-500/20",
  };

  function formatDate(dateStr: string | null) {
    if (!dateStr) return "Never";
    const d = new Date(dateStr);
    const now = new Date();
    const diff = now.getTime() - d.getTime();
    const days = Math.floor(diff / (1000 * 60 * 60 * 24));
    if (days === 0) return "Today";
    if (days === 1) return "Yesterday";
    if (days < 7) return `${days} days ago`;
    return d.toLocaleDateString();
  }

  function formatDateFull(dateStr: string | null) {
    if (!dateStr) return "Never logged in";
    const d = new Date(dateStr);
    return d.toLocaleDateString("en-US", {
      year: "numeric",
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  }

  function resetForm() {
    form = { email: "", password: "", full_name: "", phone: "", role: "admin" };
    editing = null;
  }

  function openCreate() {
    resetForm();
    showModal = true;
  }

  function openEdit(account: any) {
    form = {
      email: account.email,
      password: "",
      full_name: account.full_name,
      phone: account.phone || "",
      role: account.role,
    };
    editing = account;
    showModal = true;
  }

  async function save() {
    saving = true;
    try {
      if (editing) {
        await onUpdate(editing.id, {
          full_name: form.full_name,
          email: form.email,
          phone: form.phone || undefined,
        }, editing.role);
        toast.success("Account updated successfully");
      } else {
        await onCreate({
          email: form.email,
          password: form.password,
          full_name: form.full_name,
          phone: form.phone || undefined,
          role: form.role,
        });
        toast.success("Account created successfully");
      }
      showModal = false;
      resetForm();
      await load();
    } catch (err: any) {
      toast.error(err.message);
    } finally {
      saving = false;
    }
  }

  async function deleteAccount(account: any) {
    const confirmed = await confirmAction({
      title: "Delete Account",
      message: `Are you sure you want to delete "${account.full_name}"? This action cannot be undone.`,
      confirmLabel: "Delete",
      variant: "danger",
    });
    if (!confirmed) return;
    try {
      await onDelete(account.id, account.role);
      accounts = accounts.filter((a) => a.id !== account.id);
      toast.success("Account deleted successfully");
    } catch (err: any) {
      toast.error(err.message);
    }
  }

  function openPasswordReset(account: any) {
    passwordTarget = account;
    newPassword = "";
    showPasswordModal = true;
  }

  async function resetPassword() {
    if (!newPassword || newPassword.length < 6) {
      toast.error("Password must be at least 6 characters");
      return;
    }
    saving = true;
    try {
      await onResetPassword(passwordTarget.id, newPassword);
      toast.success("Password reset successfully");
      showPasswordModal = false;
      passwordTarget = null;
      newPassword = "";
    } catch (err: any) {
      toast.error(err.message);
    } finally {
      saving = false;
    }
  }

  const tabs = [
    { id: "all" as const, label: "All" },
    { id: "admin" as const, label: "Admin" },
    { id: "staff" as const, label: "Staff" },
  ];

  onMount(() => {
    load();
  });
</script>

<div>
  <div class="flex items-center justify-between mb-6">
    <h1 class="font-headline-h2 text-headline-h2 text-ivory-white">Account Management</h1>
    <button
      onclick={openCreate}
      class="bg-flame-orange hover:bg-flame-hover text-ivory-white px-5 py-2.5 rounded-full font-bold text-sm flex items-center gap-2 transition-all cursor-pointer"
    >
      <Plus size={16} />
      Add Account
    </button>
  </div>

  <div class="relative mb-4">
    <Search size={16} class="absolute left-4 top-1/2 -translate-y-1/2 text-muted-gray" />
    <input
      class="w-full bg-surface-charcoal border border-deep-border rounded-xl pl-10 pr-4 py-3 text-sm focus:border-flame-orange outline-none text-ivory-white placeholder:text-muted-gray"
      placeholder="Search by name or email..."
      bind:value={searchQuery}
    />
  </div>

  <div class="flex items-center gap-1 mb-6 bg-surface-charcoal rounded-xl p-1 w-fit">
    {#each tabs as tab}
      <button
        onclick={() => roleFilter = tab.id}
        class="px-4 py-2 rounded-lg text-sm font-medium transition-all cursor-pointer {roleFilter === tab.id ? 'bg-flame-orange text-ivory-white' : 'text-muted-gray hover:text-ivory-white'}"
      >
        {tab.label}
        <span class="ml-1.5 text-xs opacity-70">({counts[tab.id]})</span>
      </button>
    {/each}
  </div>

  {#if loading}
    <div class="bg-surface-card rounded-2xl border border-deep-border p-12 text-center">
      <Loader2 size={24} class="animate-spin text-muted-gray mx-auto" />
      <p class="text-muted-gray text-sm mt-2">Loading...</p>
    </div>
  {:else if filtered.length === 0}
    <div class="bg-surface-card rounded-2xl border border-deep-border p-12 text-center">
      <p class="text-muted-gray">{accounts.length === 0 ? "No accounts found" : "No accounts match your search"}</p>
    </div>
  {:else}
    <div class="bg-surface-card rounded-2xl border border-deep-border overflow-hidden">
      <table class="w-full text-sm">
        <thead>
          <tr class="border-b border-deep-border">
            <th class="text-left py-3 px-4 text-muted-gray font-medium text-[10px] uppercase tracking-wider">Account</th>
            <th class="text-left py-3 px-4 text-muted-gray font-medium text-[10px] uppercase tracking-wider hidden md:table-cell">Email</th>
            <th class="text-left py-3 px-4 text-muted-gray font-medium text-[10px] uppercase tracking-wider">Role</th>
            <th class="text-left py-3 px-4 text-muted-gray font-medium text-[10px] uppercase tracking-wider hidden lg:table-cell">Phone</th>
            <th class="text-left py-3 px-4 text-muted-gray font-medium text-[10px] uppercase tracking-wider">Status</th>
            <th class="text-left py-3 px-4 text-muted-gray font-medium text-[10px] uppercase tracking-wider hidden lg:table-cell">Last Login</th>
            <th class="text-right py-3 px-4 text-muted-gray font-medium text-[10px] uppercase tracking-wider">Actions</th>
          </tr>
        </thead>
        <tbody>
          {#each filtered as account (account.id)}
            <tr class="border-b border-deep-border/50 hover:bg-surface-charcoal/40 transition-colors">
              <td class="py-3 px-4">
                <div class="flex items-center gap-3">
                  <div class="w-9 h-9 rounded-full bg-flame-orange/20 flex items-center justify-center flex-shrink-0">
                    <span class="text-xs font-bold text-flame-orange">{getInitials(account.full_name)}</span>
                  </div>
                  <div>
                    <p class="text-ivory-white font-medium text-sm">{account.full_name}</p>
                    <p class="text-muted-gray text-xs md:hidden">{account.email}</p>
                  </div>
                </div>
              </td>
              <td class="py-3 px-4 text-ivory-white text-sm hidden md:table-cell">{account.email}</td>
              <td class="py-3 px-4">
                <span
                  class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border {roleColors[account.role] || 'bg-gray-500/10 text-gray-400 border-gray-500/20'}"
                >
                  {account.role === "admin" ? "Admin" : "Staff"}
                </span>
              </td>
              <td class="py-3 px-4 text-muted-gray text-sm hidden lg:table-cell">{account.phone || "—"}</td>
              <td class="py-3 px-4">
                <span
                  class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-medium border {statusColors[String(account.is_active)]}"
                >
                  <span class="w-1.5 h-1.5 rounded-full currentColor"></span>
                  {statusLabels[String(account.is_active)]}
                </span>
              </td>
              <td class="py-3 px-4 text-muted-gray text-xs hidden lg:table-cell" title={formatDateFull(account.last_login)}>
                {formatDate(account.last_login)}
              </td>
              <td class="py-3 px-4 text-right">
                <div class="flex items-center justify-end gap-1">
                  <button
                    onclick={() => openEdit(account)}
                    class="p-1.5 rounded-lg hover:bg-flame-orange/10 text-muted-gray hover:text-flame-orange transition-colors cursor-pointer"
                    title="Edit"
                  >
                    <Pencil size={14} />
                  </button>
                  <button
                    onclick={() => openPasswordReset(account)}
                    class="p-1.5 rounded-lg hover:bg-blue-500/10 text-muted-gray hover:text-blue-400 transition-colors cursor-pointer"
                    title="Reset Password"
                  >
                    <KeyRound size={14} />
                  </button>
                  <button
                    onclick={() => deleteAccount(account)}
                    class="p-1.5 rounded-lg hover:bg-red-500/10 text-muted-gray hover:text-red-400 transition-colors cursor-pointer"
                    title="Delete"
                  >
                    <Trash2 size={14} />
                  </button>
                </div>
              </td>
            </tr>
          {/each}
        </tbody>
      </table>
    </div>
  {/if}
</div>

<!-- Create/Edit Modal -->
{#if showModal}
  <!-- svelte-ignore a11y_no_static_element_interactions -->
  <div
    class="fixed inset-0 bg-black/60 flex items-center justify-center z-[9999] p-4"
    onclick={() => { showModal = false; resetForm(); }}
    onkeydown={(e) => { if (e.key === "Escape") { showModal = false; resetForm(); } }}
    role="dialog"
    aria-modal="true"
    tabindex="-1"
  >
    <!-- svelte-ignore a11y_no_static_element_interactions -->
    <div
      class="bg-surface-card rounded-3xl p-6 w-full max-w-md"
      onclick={(e: Event) => e.stopPropagation()}
      onkeydown={() => {}}
    >
      <div class="flex items-center justify-between mb-6">
        <h2 class="text-ivory-white font-bold text-lg">
          {editing ? "Edit" : "Create"} Account
        </h2>
        <button
          onclick={() => { showModal = false; resetForm(); }}
          class="p-1 rounded-lg hover:bg-surface-charcoal text-muted-gray hover:text-ivory-white transition-colors cursor-pointer"
        >
          <X size={18} />
        </button>
      </div>

      <div class="flex flex-col gap-4">
        <div>
          <label for="acc-fullname" class="block text-sm text-muted-gray mb-1">Full Name</label>
          <input
            id="acc-fullname"
            class="w-full bg-surface-charcoal border border-deep-border rounded-xl px-4 py-3 text-sm focus:border-flame-orange outline-none text-ivory-white"
            placeholder="Full Name"
            bind:value={form.full_name}
          />
        </div>
        <div>
          <label for="acc-email" class="block text-sm text-muted-gray mb-1">Email</label>
          <input
            id="acc-email"
            class="w-full bg-surface-charcoal border border-deep-border rounded-xl px-4 py-3 text-sm focus:border-flame-orange outline-none text-ivory-white"
            placeholder="Email"
            type="email"
            bind:value={form.email}
          />
        </div>
        {#if !editing}
          <div>
            <label for="acc-password" class="block text-sm text-muted-gray mb-1">Password</label>
            <input
              id="acc-password"
              class="w-full bg-surface-charcoal border border-deep-border rounded-xl px-4 py-3 text-sm focus:border-flame-orange outline-none text-ivory-white"
              placeholder="Password"
              type="password"
              bind:value={form.password}
            />
          </div>
          <div>
            <label for="acc-role" class="block text-sm text-muted-gray mb-1">Role</label>
            <select
              id="acc-role"
              class="w-full bg-surface-charcoal border border-deep-border rounded-xl px-4 py-3 text-sm focus:border-flame-orange outline-none text-ivory-white cursor-pointer"
              bind:value={form.role}
            >
              <option value="admin">Admin</option>
              <option value="staff">Staff</option>
            </select>
          </div>
        {/if}
        <div>
          <label for="acc-phone" class="block text-sm text-muted-gray mb-1">Phone</label>
          <input
            id="acc-phone"
            class="w-full bg-surface-charcoal border border-deep-border rounded-xl px-4 py-3 text-sm focus:border-flame-orange outline-none text-ivory-white"
            placeholder="Phone (optional)"
            bind:value={form.phone}
          />
        </div>

        {#if editing}
          <div class="bg-surface-charcoal rounded-xl p-3">
            <p class="text-xs text-muted-gray">
              To change password, use the <strong>Reset Password</strong> action from the table.
            </p>
          </div>
        {/if}

        <div class="flex gap-3 mt-2">
          <button
            onclick={() => { showModal = false; resetForm(); }}
            class="flex-1 bg-surface-charcoal hover:bg-deep-border text-ivory-white py-3 rounded-full font-bold text-sm transition-all cursor-pointer"
          >
            Cancel
          </button>
          <button
            onclick={save}
            disabled={saving || !form.full_name || !form.email || (!editing && !form.password)}
            class="flex-1 bg-flame-orange hover:bg-flame-hover text-ivory-white py-3 rounded-full font-bold text-sm transition-all cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {#if saving}
              <Loader2 size={16} class="animate-spin mx-auto" />
            {:else}
              {editing ? "Update" : "Create"}
            {/if}
          </button>
        </div>
      </div>
    </div>
  </div>
{/if}

<!-- Reset Password Modal -->
{#if showPasswordModal && passwordTarget}
  <!-- svelte-ignore a11y_no_static_element_interactions -->
  <div
    class="fixed inset-0 bg-black/60 flex items-center justify-center z-[9999] p-4"
    onclick={() => { showPasswordModal = false; passwordTarget = null; }}
    onkeydown={(e) => { if (e.key === "Escape") { showPasswordModal = false; passwordTarget = null; } }}
    role="dialog"
    aria-modal="true"
    tabindex="-1"
  >
    <!-- svelte-ignore a11y_no_static_element_interactions -->
    <div
      class="bg-surface-card rounded-3xl p-6 w-full max-w-md"
      onclick={(e: Event) => e.stopPropagation()}
      onkeydown={() => {}}
    >
      <div class="flex items-center justify-between mb-6">
        <h2 class="text-ivory-white font-bold text-lg">Reset Password</h2>
        <button
          onclick={() => { showPasswordModal = false; passwordTarget = null; }}
          class="p-1 rounded-lg hover:bg-surface-charcoal text-muted-gray hover:text-ivory-white transition-colors cursor-pointer"
        >
          <X size={18} />
        </button>
      </div>

      <p class="text-muted-gray text-sm mb-4">
        Reset password for <span class="text-ivory-white font-medium">{passwordTarget.full_name}</span>
      </p>

      <div class="flex flex-col gap-4">
        <div>
          <label for="reset-password" class="block text-sm text-muted-gray mb-1">New Password</label>
          <input
            id="reset-password"
            class="w-full bg-surface-charcoal border border-deep-border rounded-xl px-4 py-3 text-sm focus:border-flame-orange outline-none text-ivory-white"
            placeholder="Enter new password (min. 6 characters)"
            type="password"
            bind:value={newPassword}
          />
        </div>

        <div class="flex gap-3 mt-2">
          <button
            onclick={() => { showPasswordModal = false; passwordTarget = null; }}
            class="flex-1 bg-surface-charcoal hover:bg-deep-border text-ivory-white py-3 rounded-full font-bold text-sm transition-all cursor-pointer"
          >
            Cancel
          </button>
          <button
            onclick={resetPassword}
            disabled={saving || !newPassword || newPassword.length < 6}
            class="flex-1 bg-blue-500 hover:bg-blue-600 text-white py-3 rounded-full font-bold text-sm transition-all cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {#if saving}
              <Loader2 size={16} class="animate-spin mx-auto" />
            {:else}
              Reset Password
            {/if}
          </button>
        </div>
      </div>
    </div>
  </div>
{/if}
