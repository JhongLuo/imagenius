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
    <TheInputHelperText
      v-if="helperText"
      :helper-text-id="helperTextId"
      :helper-text="helperText"
    />
  </TheLabeledInput>
</template>
