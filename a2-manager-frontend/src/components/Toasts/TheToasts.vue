<script setup lang="ts">
import type { ToastModel } from '~/composables/useToasts'

defineProps<{
  toasts: ToastModel[]
}>()
</script>

<template>
  <div
    id="toast-container"
    absolute top-5 right-5
    z10
    flex flex-col justify-center items-end
  >
    <TheToast
      v-for="toast in toasts"
      :key="toast.uuid"
      v-model="toast.isShown"
      :toast-id="toast.domId"
      :toast-type="toast.type"
      :toast-text="toast.text"
    />
  </div>
</template>
