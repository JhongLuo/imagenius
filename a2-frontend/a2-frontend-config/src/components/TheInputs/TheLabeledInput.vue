<script setup lang="ts">
defineProps<{
  inputId: string
  labelText: string
}>()

const { modelValue } = defineModel<{
  modelValue?: string | number
}>()

defineOptions({
  inheritAttrs: false,
})
</script>

<template>
  <div
    w-full
    flex flex-col items-start
  >
    <label
      :for="inputId"
      my-label
    >
      {{ labelText }}
    </label>

    <TheInput
      v-if="modelValue !== undefined"
      v-model="modelValue"
      :input-id="inputId"
      v-bind="$attrs"
    />
    <slot v-else />
  </div>
</template>
