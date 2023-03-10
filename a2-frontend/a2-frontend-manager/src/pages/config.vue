<script setup lang="ts">
defineOptions({
  name: 'ConfigPage',
})

const api = useAPIStore()
const { toastsArray, blinkToast } = useToasts()

const cacheConfigs = reactive({
  replacementPolicy: '',
  maxSize: 0,
})
const cacheKeys = ref([])
const isDownloading = ref(false)
const isModalPutCacheConfigsShown = ref(false)

const showModalPutCacheConfigs = () => {
  isModalPutCacheConfigsShown.value = true
}

const handleGetCacheConfigs = async () => {
  // fetch data
  try {
    const response = await api.getCacheConfigs()
    utilsJS.validateResponse(response)
    // handle success
    cacheConfigs.replacementPolicy = response.data.replacement_policy
    cacheConfigs.maxSize
          = response.data.max_size / (1024 ** 2) // convert to MB
    blinkToast(
      TOAST_ID__GET_CACHE_CONFIGS__SUCCESS,
      'info',
      TOAST_MSG__GET_CACHE_CONFIGS__SUCCESS)
  }
  catch (errMsg) {
    // handle error
    blinkToast(
      TOAST_ID__GET_CACHE_CONFIGS__ERROR,
      'error',
      errMsg as string)
  }
}

const handlePutCacheConfigs = async () => {
  // fetch data
  try {
    // construct request data
    const data = {
      replacement_policy: cacheConfigs.replacementPolicy,
      max_size: cacheConfigs.maxSize * (1024 ** 2), // convert to bytes
    }
    const response = await api.putCacheConfigs(data)
    utilsJS.validateResponse(response)
    // handle success
    cacheConfigs.replacementPolicy = response.data.replacement_policy
    cacheConfigs.maxSize
          = response.data.max_size / (1024 ** 2) // convert to MB
    blinkToast(
      TOAST_ID__PUT_CACHE_CONFIGS__SUCCESS,
      'success',
      TOAST_MSG__PUT_CACHE_CONFIGS__SUCCESS)
  }
  catch (errMsg) {
    // handle error
    blinkToast(
      TOAST_ID__PUT_CACHE_CONFIGS__ERROR,
      'error',
      errMsg as string)
  }
}

const handleGetCacheKeys = async (isReload = false) => {
  isDownloading.value = true
  // fetch data
  try {
    const response = await api.getCacheKeys()
    utilsJS.validateResponse(response)
    // handle success
    cacheKeys.value = response.data.keys
    await utils.sleep(150)
    isDownloading.value = false
    if (!isReload) {
      blinkToast(
        TOAST_ID__GET_CACHE_KEYS__SUCCESS,
        'info',
        TOAST_MSG__GET_CACHE_KEYS__SUCCESS)
    }
  }
  catch (errMsg) {
    // handle error
    cacheKeys.value = []
    blinkToast(
      TOAST_ID__GET_CACHE_KEYS__ERROR,
      'error',
      errMsg as string)
    isDownloading.value = false
  }
}

const handleDeleteCache = async () => {
  // fetch data
  try {
    const response = await api.postClearCache()
    utilsJS.validateResponse(response)
    // handle success
    blinkToast(
      TOAST_ID__CLEAR_CACHE__SUCCESS,
      'success',
      TOAST_MSG__CLEAR_CACHE__SUCCESS)
    await handleGetCacheKeys(true)
  }
  catch (errMsg) {
    // handle error
    blinkToast(
      TOAST_ID__CLEAR_CACHE__ERROR,
      'error',
      errMsg as string)
  }
}

onMounted(() => {
  handleGetCacheConfigs()
  handleGetCacheKeys()
})
</script>

<template>
  <!-- Page Title -->
  <h1 my-title>
    Config
  </h1>

  <!-- Page Content -->
  <ThePageContent>
    <!-- Input Group -->
    <TheInputGroup
      w-xs
      px-8 py-6
      my-bg-secondary
      my-card my-shadow-light
    >
      <!-- Replacement Policy -->
      <TheLabeledInput
        input-id="input-replacement-policy"
        label-text="Replacement Policy"
        mb-3
      >
        <select
          id="input-replacement-policy"
          v-model="cacheConfigs.replacementPolicy"
          w-full p-2.5
          text-sm my-text-color-primary
          my-input
        >
          <option disabled>
            Choose one of the following:
          </option>
          <option value="LRU">
            Least Recently Used
          </option>
          <option value="random">
            Random Replacement
          </option>
        </select>
      </TheLabeledInput>

      <!-- Max Cache Size -->
      <TheLabeledInput
        input-id="input-max-cache-size"
        label-text="Max Cache Size"
      >
        <div
          flex w-full
        >
          <input
            id="input-max-cache-size"
            v-model="cacheConfigs.maxSize"
            type="number"
            flex-grow-1
            my-border rounded-r-none
            my-input
            placeholder="Enter a number"
          >
          <span
            inline-flex items-center px-3
            my-border rounded-l-none border-l-0
            my-input select-none
          >
            MB
          </span>
        </div>
      </TheLabeledInput>

      <!-- Button: Submit New Cache Configs -->
      <TheButton
        text-sm
        label="Update"
        @click="showModalPutCacheConfigs"
      />

      <!-- Modal: Put Cache Configs -->
      <TheModal
        v-model:is-shown="isModalPutCacheConfigsShown"
        modal-type="submit"
        :modal-id="MODAL_ID__PUT_CACHE_CONFIGS"
        :modal-title="MODAL_TITLE__PUT_CACHE_CONFIGS"
        :modal-description="MODAL_DESCRIPTION__PUT_CACHE_CONFIGS(cacheConfigs.replacementPolicy, cacheConfigs.maxSize)"
        :action="handlePutCacheConfigs"
      />
    </TheInputGroup>

    <!-- HR -->
    <TheConfigHR />

    <!-- Table: All Keys -->
    <TheKeyTable
      :data="cacheKeys"
      :table-title="TABLE_TITLE__CACHE_KEYS"
      :table-description="TABLE_DESCRIPTION__CACHE_KEYS"
      :delete-button-text="TABLE_DELETE_BUTTON_TEXT__CACHE_KEYS"
      :delete-button-action="handleDeleteCache"
      :modal-id="MODAL_ID__CLEAR_CACHE"
      :modal-title="MODAL_TITLE__CLEAR_CACHE"
      :modal-description="MODAL_DESCRIPTION__CLEAR_CACHE"
      :class="{ 'blur-sm grayscale': isDownloading }"
      transition-all duration-300
    />
  </ThePageContent>

  <!-- Toasts, Alerts & Modals -->
  <TheToasts
    :toasts-array="toastsArray"
  />
</template>
