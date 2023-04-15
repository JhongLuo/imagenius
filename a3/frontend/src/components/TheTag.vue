<script setup lang="ts">
defineProps<{
  label: string
}>()

const { modelValue } = defineModel<{
  modelValue: boolean
}>()
</script>

<template>
  <span
    px-3 py-1
    w-min h-min
    backdrop-blur-sm rounded-lg
    text-white select-none cursor-pointer
    class="bg-truegray-5"
    :class="modelValue ? 'op-90' : 'op-30'"
    @click="modelValue = !modelValue"
  >
    {{ label }}
  </span>
</template>
