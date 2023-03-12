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
    utilsJS.validateResponse(response)
    // handle success
    allKeys.value = response.data.keys
    await utils.sleep(150)
    isDownloading.value = false
    if (!isReload) {
      blinkToast(
        TOAST_ID__GET_ALL_KEYS__SUCCESS,
        'info',
        TOAST_MSG__GET_ALL_KEYS__SUCCESS)
    }
  }
  catch (errMsg) {
    // handle error
    allKeys.value = []
    blinkToast(
      TOAST_ID__GET_ALL_KEYS__ERROR,
      'error',
      errMsg as string)
  }
}

const handleDeleteAll = async () => {
  // fetch data
  try {
    const response = await api.postDeleteAllData()
    utilsJS.validateResponse(response)
    // handle success
    blinkToast(
      TOAST_ID__DELETE_ALL__SUCCESS,
      'success',
      TOAST_MSG__DELETE_ALL__SUCCESS)
    await handleGetAllKeys(true)
  }
  catch (errMsg) {
    // handle error
    blinkToast(
      TOAST_ID__DELETE_ALL__ERROR,
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
  <h1 my-title>
    Keys
  </h1>

  <!-- Page Content -->
  <ThePageContent>
    <!-- Table: All Keys -->
    <TheKeyTable
      :data="allKeys"
      :table-title="TABLE_TITLE__ALL_KEYS"
      :table-description="TABLE_DESCRIPTION__ALL_KEYS"
      :delete-button-text="TABLE_DELETE_BUTTON_TEXT__ALL_KEYS"
      :delete-button-action="handleDeleteAll"
      :modal-id="MODAL_ID__DELETE_ALL"
      :modal-title="MODAL_TITLE__DELETE_ALL"
      :modal-description="MODAL_DESCRIPTION__DELETE_ALL"
      :class="{ 'blur-sm grayscale': isDownloading }"
      transition-all duration-300
    />
  </ThePageContent>

  <!-- Toasts, Alerts & Modals -->
  <TheToasts
    :toasts-array="toastsArray"
  />
</template>
