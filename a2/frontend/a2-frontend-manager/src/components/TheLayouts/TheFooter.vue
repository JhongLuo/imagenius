<script setup lang="ts">
const api = useAPIStore()
</script>

<template>
  <div flex-col space-y-3>
    <div flex justify-center items-baseline>
      <span
        my-helper-text select-none
      >
        Currently connecting to&nbsp;
      </span>
      <span
        px-1.5 py-1 rounded bg-gray-4 bg-op-15
        my-helper-text font-mono my-text-color-primary
      >
        {{ api.baseURLShort }}
      </span>
    </div>

    <!-- <TheNavs /> -->
  </div>
</template>
