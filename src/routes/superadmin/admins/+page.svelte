<script lang="ts">
  import { onMount } from "svelte";
  import { Plus } from "@lucide/svelte";
  import { toast } from "svelte-sonner";
  import { confirmAction } from "$lib/utils/confirm";
  import { api } from "$lib/api";
  import DataTable from "$lib/components/ui/DataTable.svelte";

  let admins = $state<any[]>([]);
  let loading = $state(true);
  let showForm = $state(false);
  let editing = $state<any>(null);

  let form = $state({ email: "", password: "", full_name: "", phone: "" });

  onMount(async () => {
    try {
      admins = await api.superadminListAdmins();
    } catch (err: any) {
      toast.error(err.message || "Failed to load admins");
    } finally {
      loading = false;
    }
  });

  function resetForm() {
    form = { email: "", password: "", full_name: "", phone: "" };
    editing = null;
  }

   const columns = [
     { key: "full_name", label: "Name" },
     { key: "email", label: "Email" },
     { key: "phone", label: "Phone" },
   ];

   function editAdmin(admin: any) {
     form = { email: admin.email, password: "", full_name: admin.full_name, phone: admin.phone || "" };
     editing = admin;
     showForm = true;
   }

  async function save() {
    try {
      if (editing) {
        await api.superadminUpdateAdmin(editing.id, { full_name: form.full_name, email: form.email, phone: form.phone || undefined });
        toast.success("Admin updated successfully");
      } else {
        await api.superadminCreateAdmin(form);
        toast.success("Admin created successfully");
      }
      admins = await api.superadminListAdmins();
      showForm = false;
      resetForm();
    } catch (err: any) {
      toast.error(err.message);
    }
  }

  async function deleteAdmin(admin: any) {
    const confirmed = await confirmAction({
      title: "Delete Admin",
      message: `Are you sure you want to delete "${admin.full_name}"?`,
      confirmLabel: "Delete",
      variant: "danger",
    });
    if (!confirmed) return;
    try {
      await api.superadminDeleteAdmin(admin.id);
      admins = admins.filter((a) => a.id !== admin.id);
      toast.success("Admin deleted successfully");
    } catch (err: any) {
      toast.error(err.message);
    }
  }
</script>

<div class="flex items-center justify-between mb-8">
  <h1 class="font-headline-h2 text-headline-h2 text-ivory-white">Admin Management</h1>
  <button onclick={() => { showForm = !showForm; resetForm(); }} class="bg-flame-orange hover:bg-flame-hover text-ivory-white px-5 py-2.5 rounded-full font-bold text-sm flex items-center gap-2 transition-all cursor-pointer">
    <Plus size={16} />
    {showForm ? "Cancel" : "Add Admin"}
  </button>
</div>

{#if showForm}
  <div class="bg-surface-card rounded-2xl border border-deep-border p-6 mb-8 max-w-lg">
    <h3 class="font-headline-h3 text-headline-h3 text-ivory-white mb-4">{editing ? "Edit" : "Create"} Admin</h3>
    <div class="flex flex-col gap-4">
      <input class="bg-surface-charcoal border border-deep-border rounded-xl px-4 py-3 text-sm focus:border-flame-orange outline-none text-ivory-white" placeholder="Full Name" bind:value={form.full_name} />
      <input class="bg-surface-charcoal border border-deep-border rounded-xl px-4 py-3 text-sm focus:border-flame-orange outline-none text-ivory-white" placeholder="Email" type="email" bind:value={form.email} />
      <input class="bg-surface-charcoal border border-deep-border rounded-xl px-4 py-3 text-sm focus:border-flame-orange outline-none text-ivory-white" placeholder="Password" type="password" bind:value={form.password} />
      <input class="bg-surface-charcoal border border-deep-border rounded-xl px-4 py-3 text-sm focus:border-flame-orange outline-none text-ivory-white" placeholder="Phone" bind:value={form.phone} />
      <button onclick={save} class="bg-flame-orange hover:bg-flame-hover text-ivory-white py-3 rounded-full font-bold cursor-pointer">{editing ? "Update" : "Create"}</button>
    </div>
  </div>
{/if}

<div class="bg-surface-card rounded-2xl border border-deep-border p-6">
  <DataTable {columns} rows={admins} {loading} onEdit={editAdmin} onDelete={deleteAdmin} />
</div>
