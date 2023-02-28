<script setup lang="ts">
const { modelValue } = defineModel<{
  modelValue: string
}>()
</script>

<template>
  <input
    v-model="modelValue"
    v-bind="$attrs"
    type="text"
    my-text-input-style
    autocomplete="false"
  >
</template>
