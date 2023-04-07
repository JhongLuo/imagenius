<script setup lang="ts">
import type { Labeled, Selectable } from '~/composables/utils'

const { modelValue } = defineModel<{
  modelValue: (Labeled & Selectable)[]
}>()
</script>

<template>
  <div
    w-md
    flex flex-wrap justify-center gap-1
  >
    <TheTag
      v-for="tag in modelValue"
      :key="tag.label"
      v-model="tag.selected"
      :label="tag.label"
    />
  </div>
</template>
