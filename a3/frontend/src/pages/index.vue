<script setup lang="ts" generic="T extends any, O extends any">
defineOptions({
  name: 'IndexPage',
})

const api = useAPIStore()

const start = () => {
  api.updateApiKey()
  window.location.href = '/add'
}
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
    <div>
      <TheIconedTextInput
        v-model.trim="api.ipAddr.addr"
        w-64
        icon="i-carbon-connection-signal"
        input-id="input-api-ip-addr"
        placeholder="Where to connect?"
        @keydown.enter="start"
      />
    </div>

    <!-- input: api key -->
    <div
      mt-4
    >
      <TheIconedTextInput
        v-model.trim="api.apiKey"
        w-64
        icon="i-carbon-password"
        input-id="input-api-key"
        placeholder="Your api key"
        @keydown.enter="start"
      />
    </div>

    <!-- button: go -->
    <button
      my-btn-primary mt-8 text-sm
      :disabled="!api.ipAddr.addr || !api.apiKey"
      @click="start"
    >
      Go
    </button>
  </ThePageContent>
</template>
