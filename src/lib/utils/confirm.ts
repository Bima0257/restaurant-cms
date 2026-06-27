import { writable } from "svelte/store";
import { get } from "svelte/store";

interface DialogState {
  title: string;
  message: string;
  confirmLabel: string;
  cancelLabel: string;
  variant: "danger" | "primary";
  resolve: (value: boolean) => void;
  open: boolean;
}

const dialogStore = writable<DialogState | null>(null);

export function confirmAction(options: {
  title: string;
  message: string;
  confirmLabel?: string;
  cancelLabel?: string;
  variant?: "danger" | "primary";
}): Promise<boolean> {
  return new Promise((resolve) => {
    dialogStore.set({
      title: options.title,
      message: options.message,
      confirmLabel: options.confirmLabel || "Confirm",
      cancelLabel: options.cancelLabel || "Cancel",
      variant: options.variant || "primary",
      resolve,
      open: true,
    });
  });
}

export function getDialogState() {
  return {
    subscribe: dialogStore.subscribe,
    confirm() {
      const state = get(dialogStore);
      state?.resolve(true);
      dialogStore.set(null);
    },
    cancel() {
      const state = get(dialogStore);
      state?.resolve(false);
      dialogStore.set(null);
    },
  };
}
