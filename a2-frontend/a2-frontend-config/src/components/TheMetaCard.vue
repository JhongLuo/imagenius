<script setup lang="ts">
defineProps<{
  isBlurred: boolean
}>()
</script>

<template>
  <div
    w-full
    px-8 py-6
    my-bg-secondary
    my-card my-shadow-light
    :class="{
      'blur-sm grayscale': isBlurred,
    }"
    transition-all duration-300
    space-y-1
  >
    <slot />
  </div>
</template>
