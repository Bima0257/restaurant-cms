<script lang="ts">
  import { api } from "$lib/api";
  import AccountTable from "$lib/components/superadmin/AccountTable.svelte";
</script>

<AccountTable
  apiList={api.superadminListAccounts}
  onCreate={(data: any) =>
    data.role === "admin"
      ? api.superadminCreateAdmin(data)
      : api.superadminCreateStaff(data)
  }
  onUpdate={(id: number, data: any, role: string) =>
    role === "admin"
      ? api.superadminUpdateAdmin(id, data)
      : api.superadminUpdateStaff(id, data)
  }
  onDelete={(id: number, role: string) =>
    role === "admin"
      ? api.superadminDeleteAdmin(id)
      : api.superadminDeleteStaff(id)
  }
  onResetPassword={api.superadminResetPassword}
  onToggleStatus={api.superadminToggleAccountStatus}
/>
