<script setup lang="ts">
defineProps<{
  labelText: string
  inputId: string
  helperTextId?: string
  helperText?: string
}>()

defineOptions({
  inheritAttrs: false,
})
</script>

<template>
  <TheLabeledInput
    :input-id="inputId"
    :label-text="labelText"
  >
    <TheInput
      :input-id="inputId"
      type="file"
      w-full block cursor-pointer
      text-xs
      my-input
      :aria-describedby="helperTextId"
      v-bind="$attrs"
    />
    <p
      v-if="helperText"
      :id="helperTextId"
      my-helper-text
    >
      {{ helperText }}
    </p>
  </TheLabeledInput>
</template>
