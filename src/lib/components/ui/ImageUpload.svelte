<script lang="ts">
  import { Upload, X, Loader2 } from "@lucide/svelte";
  import { toast } from "svelte-sonner";
  import { api } from "$lib/api";

  interface Props {
    currentUrl?: string;
    onUpload: (url: string) => void;
    label?: string;
  }

  let { currentUrl = "", onUpload, label = "Upload Image" }: Props = $props();

  let preview = $state(currentUrl);
  let loading = $state(false);

  const ACCEPTED_TYPES = ["image/jpeg", "image/png", "image/webp"];
  const MAX_SIZE = 2 * 1024 * 1024;

  function validate(file: File): string | null {
    if (!ACCEPTED_TYPES.includes(file.type)) {
      return "Only JPG, PNG, and WEBP files are allowed";
    }
    if (file.size > MAX_SIZE) {
      return "File must be under 2 MB";
    }
    return null;
  }

  async function handleFileChange(e: Event) {
    const input = e.target as HTMLInputElement;
    const file = input.files?.[0];
    if (!file) return;

    const validationError = validate(file);
    if (validationError) {
      toast.error(validationError);
      input.value = "";
      return;
    }

    preview = URL.createObjectURL(file);
    loading = true;
    try {
      const res = await api.upload(file);
      onUpload(res.data.url);
    } catch (err: any) {
      toast.error(err.message);
      preview = currentUrl;
    } finally {
      loading = false;
      input.value = "";
    }
  }

  function remove() {
    preview = "";
    onUpload("");
  }
</script>

<div class="flex flex-col gap-2">
  {#if label}
    <span class="text-sm text-muted-gray">{label}</span>
  {/if}

  {#if preview}
    <div class="relative w-32 h-32 rounded-xl overflow-hidden border border-deep-border">
      <img src={preview} alt="Preview" class="w-full h-full object-cover" />
      <button
        onclick={remove}
        disabled={loading}
        class="absolute top-1 right-1 bg-black/60 text-white p-1 rounded-full hover:bg-black/80 transition-colors disabled:opacity-50 cursor-pointer"
      >
        <X size={14} />
      </button>
      {#if loading}
        <div class="absolute inset-0 bg-black/40 flex items-center justify-center">
          <Loader2 size={24} class="text-ivory-white animate-spin" />
        </div>
      {/if}
    </div>
  {:else}
    <label class="flex flex-col items-center justify-center w-32 h-32 rounded-xl border-2 border-dashed border-deep-border bg-surface-charcoal hover:border-flame-orange transition-colors cursor-pointer">
      <Upload size={24} class="text-muted-gray mb-1" />
      <span class="text-xs text-muted-gray">Click to upload</span>
      <input
        type="file"
        accept=".jpg,.jpeg,.png,.webp"
        onchange={handleFileChange}
        class="hidden"
        disabled={loading}
      />
    </label>
  {/if}
</div>
