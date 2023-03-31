<script setup lang="ts">
const api = useAPIStore()
const { latestNumNodes, uninitializedLnnVal } = useLatestNumNodes()
const { toastsArray, blinkToast } = useToasts()

const handleMonitorNumNodesChange = async () => {
  while (true) {
    // start listening
    try {
      const response = await api.getNumNodes()
      utilsJS.validateResponse(response)
      // handle success
      const newNumNodes = response.data.numNodes
      if (latestNumNodes.value !== newNumNodes) {
        // ignore the first change from uninitialized LNN
        if (latestNumNodes.value !== uninitializedLnnVal) {
        // found new change
          blinkToast(
            TOAST_ID__NEW_NUM_NODES,
            'info',
            TOAST_MSG__NEW_NUM_NODES(latestNumNodes.value, newNumNodes))
        }
        // update LNN
        latestNumNodes.value = newNumNodes
      }
    }
    catch (errMsg) {
    // handle error
      blinkToast(
        TOAST_ID__GET_NUM_NODES__ERROR,
        'error',
        errMsg as string)
    }

    // refresh every 5 seconds
    await utils.sleep(5000)
  }
}

onMounted(() => {
  // start listening
  handleMonitorNumNodesChange()
})
</script>

<template>
  <main
    min-h-screen px-4 py-10
    flex flex-col justify-between items-center
    font-sans
    text-center
  >
    <!-- header + content -->
    <div>
      <TheHeader />

      <!-- spacer -->
      <div py-5 />

      <RouterView />
    </div>

    <!-- footer -->
    <footer flex-col mt-16>
      <TheFooter />
    </footer>
  </main>

  <!-- Toasts -->
  <TheToasts
    :toasts-array="toastsArray"
    toasts-pos="bottom"
  />
</template>
