<script setup lang="ts">
defineOptions({
  name: 'KeysPage',
})

const api = useAPIStore()
const { toastsArray, blinkToast } = useToasts()

const keys = ref([])
const isDownloading = ref(false)

const handleGetKeys = async (isReload = false) => {
  isDownloading.value = true
  // fetch data
  try {
    const response = await api.getAllKeys()
    utils.validateResponse(response)
    // handle success
    keys.value = response.data.keys
    await utils.sleep(150)
    isDownloading.value = false
    if (!isReload) {
      blinkToast(
        TOAST_ID_SUCCESS_GET_ALL_KEYS,
        'info',
        MSG_SUCCESS_GET_ALL_KEYS)
    }
  }
  catch (errMsg) {
    // handle error
    keys.value = []
    blinkToast(
      TOAST_ID_ERROR_GET_ALL_KEYS,
      'error',
      errMsg as string)
    isDownloading.value = false
  }
}

const handleDeleteAll = async () => {
  // fetch data
  try {
    const response = await api.postDeleteAllData()
    utils.validateResponse(response)
    // handle success
    blinkToast(
      TOAST_ID_SUCCESS_DELETE_ALL_KEYS,
      'success',
      MSG_SUCCESS_DELETE_ALL_KEYS)
    await handleGetKeys(true)
  }
  catch (errMsg) {
    // handle error
    blinkToast(
      TOAST_ID_ERROR_DELETE_ALL_KEYS,
      'error',
      errMsg as string)
  }
}

onMounted(() => {
  handleGetKeys()
})
</script>

<template>
  <!-- Page Title -->
  <h1 my-title-style>
    Keys
  </h1>

  <!-- Page Content -->
  <ThePageContent>
    <!-- Table: All Keys -->
    <TheKeyTable
      caption-title="All Keys"
      caption-content="from database + mem-cache"
      :keys="keys"
      :delete-action="handleDeleteAll"
      :class="{ 'blur-sm': isDownloading }"
      transition-all duration-300
    />
  </ThePageContent>

  <!-- Toasts, Alerts & Modals -->
  <TheToasts
    :toasts-array="toastsArray"
  />
</template>
