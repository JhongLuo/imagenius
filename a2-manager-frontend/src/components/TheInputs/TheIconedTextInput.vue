<script setup lang="ts">
defineProps<{
  icon: string
  inputId: string
}>()

const { modelValue } = defineModel<{
  modelValue: string
}>()

defineOptions({
  inheritAttrs: false,
})
</script>

<template>
  <div
    w-full
    relative mb-4 flex justify-start
  >
    <div
      absolute inset-y-0 left-0 pl-3
      flex items-center cursor-default
    >
      <span
        icon-plain
        :class="icon"
      />
    </div>

    <TheTextInput
      v-model="modelValue"
      :input-id="inputId"
      pl-10
      v-bind="$attrs"
    />
  </div>
</template>
