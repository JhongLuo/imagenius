<script setup lang="ts" generic="T extends any, O extends any">
import { initTooltips } from 'flowbite'

defineOptions({
  name: 'IndexPage',
})

onMounted(() => {
  initTooltips()
})

const api = useAPIStore()

const navigateToUpload = () => {
  window.location.href = '/upload'
}
</script>

<template>
  <div mt-8>
    <TheTextInput
      v-model="api.ipAddr.addr"
      text-center
      placeholder="Where to connect?"
      data-tooltip-target="tooltip-no-arrow"
      data-tooltip-trigger="hover"
      @keydown.enter="navigateToUpload"
    />
    <div
      id="tooltip-no-arrow"
      role="tooltip"
      class="absolute z-10 invisible inline-block px-3 py-2 text-sm font-medium text-white bg-gray-900 rounded-lg shadow-sm opacity-0 tooltip dark:bg-gray-700"
    >
      Where to connect?
    </div>

    <div>
      <button
        my-btn-primary m-3 text-sm
        :disabled="!api.ipAddr.addr"
        @click="navigateToUpload"
      >
        Go
      </button>
    </div>
  </div>
</template>
