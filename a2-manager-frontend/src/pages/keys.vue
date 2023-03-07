<script setup lang="ts">
defineOptions({
  name: 'KeysPage',
})

const api = useAPIStore()
const { toastsArray, blinkToast } = useToasts()

const keys = ref([])
const isDownloading = ref(false)

const handleGetKeys = async () => {
  // < input validation already done by button disabled state >
  isDownloading.value = true
  // fetch data
  try {
    const response = await api.getAllKeys()
    utils.validateResponse(response)
    // handle success
    keys.value = response.data.keys
    setTimeout(() => {
      // short delay to show blur effect
      isDownloading.value = false
      blinkToast(
        TOAST_ID_GET_ALL_KEYS_SUCCESS,
        'info',
        MSG_SUCCESS_GET_ALL_KEYS)
    }, 100)
  }
  catch (errMsg) {
    // handle error
    keys.value = []
    blinkToast(
      TOAST_ID_GET_ALL_KEYS_ERROR,
      'error',
      errMsg as string)
    isDownloading.value = false
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
  <div
    w-sm
    flex flex-col items-center
  >
    <!-- Table: All Keys -->
    <TheKeyTable
      caption-title="All Keys"
      caption-content="from database + mem-cache"
      :keys="keys"
      :class="{ 'blur-sm': isDownloading }"
      transition-all duration-400
    />
  </div>
  <!-- Toasts, Alerts & Modals -->
  <TheToasts
    :toasts-array="toastsArray"
  />
</template>
