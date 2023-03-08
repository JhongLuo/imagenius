<script setup lang="ts">
defineOptions({
  name: 'KeysPage',
})

const api = useAPIStore()
const { toastsArray, blinkToast } = useToasts()

const allKeys = ref([])
const isDownloading = ref(false)

const handleGetAllKeys = async (isReload = false) => {
  isDownloading.value = true
  // fetch data
  try {
    const response = await api.getAllKeys()
    utils.validateResponse(response)
    // handle success
    allKeys.value = response.data.keys
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
    allKeys.value = []
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
      TOAST_ID_SUCCESS_DELETE_ALL,
      'success',
      MSG_SUCCESS_DELETE_ALL)
    await handleGetAllKeys(true)
  }
  catch (errMsg) {
    // handle error
    blinkToast(
      TOAST_ID_ERROR_DELETE_ALL,
      'error',
      errMsg as string)
  }
}

onMounted(() => {
  handleGetAllKeys()
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
      :data="allKeys"
      :table-title="TABLE_TITLE_ALL_KEYS"
      :table-description="TABLE_DESCRIPTION_ALL_KEYS"
      :delete-button-text="TABLE_DELETE_BUTTON_TEXT_ALL_KEYS"
      :delete-button-action="handleDeleteAll"
      :modal-id="MODAL_ID_DELETE_ALL"
      :modal-title="MODAL_TITLE_DELETE_ALL"
      :modal-description="MODAL_DESCRIPTION_DELETE_ALL"
      :class="{ 'blur-sm grayscale': isDownloading }"
      transition-all duration-300
    />
  </ThePageContent>

  <!-- Toasts, Alerts & Modals -->
  <TheToasts
    :toasts-array="toastsArray"
  />
</template>
