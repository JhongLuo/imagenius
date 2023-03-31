<script setup lang="ts">
defineProps<{
  inputId: string
}>()

const { modelValue } = defineModel<{
  modelValue: string | number
}>()
</script>

<template>
  <input
    :id="inputId"
    v-model="modelValue"
    my-input
    autocomplete="off"
  >
</template>
