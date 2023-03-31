<script setup lang="ts">
defineProps<{
  helperTextId?: string
  helperText?: string
}>()
</script>

<template>
  <p
    :id="helperTextId"
    my-helper-text
  >
    {{ helperText }}
  </p>
</template>
