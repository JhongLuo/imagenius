<script setup lang="ts" generic="T extends any, O extends any">
import { initTooltips } from 'flowbite'

defineOptions({
  name: 'IndexPage',
})

const api = useAPIStore()

const navigateToUpload = () => {
  window.location.href = '/upload'
}

onMounted(() => {
  initTooltips()
})
</script>

<template>
  <!-- Page Title -->
  <h1 my-title-style>
    Connect
  </h1>

  <!-- Page Content -->
  <div mt-12>
    <!-- input: connection target -->
    <TheTextInput
      v-model="api.ipAddr.addr"
      input-id="api-ip-addr"
      text-center
      placeholder="Where to connect?"
      data-tooltip-target="tooltip-no-arrow"
      data-tooltip-trigger="hover"
      @keydown.enter="navigateToUpload"
    />

    <!-- tooltip -->
    <div
      id="tooltip-no-arrow"
      role="tooltip"
      class="invisible"
      inline-block z-10
      px-3 py-2
      text-xs font-medium
      rounded-lg shadow-lg shadow-gray-400 shadow-op-80 dark:shadow-gray-700 dark:shadow-op-30
      text-white bg-gray-400 dark:bg-gray-800
    >
      Where to connect?
    </div>

    <!-- button: go -->
    <button
      my-btn-primary m-3 text-sm
      :disabled="!api.ipAddr.addr"
      @click="navigateToUpload"
    >
      Go
    </button>
  </div>
</template>
