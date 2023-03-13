<script setup lang="ts">
defineProps<{
  inputId: string
}>()

const { modelValue } = defineModel<{
  modelValue: string
}>()
</script>

<template>
  <TheInput
    v-model="modelValue"
    :input-id="inputId"
    type="text"
  />
</template>
