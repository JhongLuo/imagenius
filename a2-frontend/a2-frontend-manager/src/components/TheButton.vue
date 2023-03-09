<script setup lang="ts">
defineProps<{
  label: string
}>()
</script>

<template>
  <button
    my-btn-primary
  >
    {{ label }}
  </button>
</template>
