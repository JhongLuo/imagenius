<script setup lang="ts" generic="T extends any, O extends any">
defineOptions({
  name: 'IndexPage',
})

const api = useAPIStore()

const start = () => {
  window.location.href = '/meta'
}

onMounted(() => {
  initTooltips()
})
</script>

<template>
  <!-- Page Title -->
  <h1 my-title>
    Connect
  </h1>

  <!-- Page Content -->
  <ThePageContent
    mt-12
  >
    <!-- input: connection target -->
    <TheTextInput
      v-model="api.ipAddr.addr"
      input-id="api-ip-addr"
      placeholder="Where to connect?"
      data-tooltip-target="tooltip-connect"
      data-tooltip-trigger="hover"
      w-64 text-center
      @keydown.enter="start"
    />

    <!-- tooltip -->
    <TheTooltip
      id="tooltip-connect"
      label="Where to connect?"
    />

    <!-- button: go -->
    <button
      my-btn-primary m-4 text-sm
      :disabled="!api.ipAddr.addr"
      @click="start"
    >
      Go
    </button>
  </ThePageContent>
</template>
