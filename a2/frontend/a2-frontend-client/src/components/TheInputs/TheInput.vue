<script setup lang="ts">
defineProps<{
  inputId: string
}>()

const { modelValue } = defineModel<{
  modelValue?: string
}>()
</script>

<template>
  <input
    :id="inputId"
    v-model="modelValue"
    my-input-style
    autocomplete="false"
  >
</template>
