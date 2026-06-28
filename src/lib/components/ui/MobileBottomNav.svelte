<script lang="ts">
  import { page } from "$app/stores";

  interface BottomNavItem {
    label: string;
    href: string;
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    icon: any;
  }

  let {
    items,
    isActive,
    class: className = "",
  }: {
    items: BottomNavItem[];
    isActive?: (href: string) => boolean;
    class?: string;
  } = $props();

  function getActive(href: string): boolean {
    return isActive ? isActive(href) : $page.url.pathname === href;
  }
</script>

<div
  class="md:hidden fixed bottom-0 left-0 w-full bg-surface-container-lowest/80 backdrop-blur-lg border-t border-deep-border flex justify-around items-center py-3 px-2 z-50 {className}"
>
  {#each items as item}
    <a
      href={item.href}
      class="flex flex-col items-center gap-1 {getActive(item.href) ? 'text-flame-orange' : 'text-muted-gray'}"
    >
      <item.icon size={20} />
      <span class="text-[10px] font-bold">{item.label}</span>
    </a>
  {/each}
</div>
