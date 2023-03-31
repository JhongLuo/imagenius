<script setup lang="ts">
defineProps<{
  id: string
  label: string
}>()
</script>

<template>
  <div
    :id="id"
    role="tooltip"
    class="invisible"
    inline-block z-10
    px-3 py-2
    text-xs font-medium
    my-card
    text-white bg-gray-400 dark:bg-gray-800
  >
    {{ label }}
  </div>
</template>
