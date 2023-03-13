<script setup lang="ts">
defineProps<{
  toastsArray: ToastModel[]
  toastsPos?: 'top' | 'bottom'
}>()
</script>

<template>
  <div
    id="toast-container"
    fixed
    :class="{
      'top-5 right-5': !toastsPos || toastsPos === 'top',
      'bottom-5 right-5': toastsPos === 'bottom',
    }"
    z10
    flex flex-col justify-center items-end
  >
    <TheToast
      v-for="toast in toastsArray"
      :key="toast.uuid"
      v-model:isShown="toast.isShown"
      :toast-id="toast.domId"
      :toast-type="toast.type"
      :toast-text="toast.text"
    />
  </div>
</template>
