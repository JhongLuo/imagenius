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
    utils.validateResponse(response)
    // handle success
    cacheConfigs.replacementPolicy = response.data.replacement_policy
    cacheConfigs.maxSize
          = response.data.max_size / (1024 ** 2) // convert to MB
    blinkToast(
      TOAST_ID_SUCCESS_GET_CACHE_CONFIGS,
      'info',
      MSG_SUCCESS_GET_CACHE_CONFIGS)
  }
  catch (errMsg) {
    // handle error
    blinkToast(
      TOAST_ID_ERROR_GET_CACHE_CONFIGS,
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
    utils.validateResponse(response)
    // handle success
    cacheConfigs.replacementPolicy = response.data.replacement_policy
    cacheConfigs.maxSize
          = response.data.max_size / (1024 ** 2) // convert to MB
    blinkToast(
      TOAST_ID_SUCCESS_PUT_CACHE_CONFIGS,
      'success',
      MSG_SUCCESS_PUT_CACHE_CONFIGS)
  }
  catch (errMsg) {
    // handle error
    blinkToast(
      TOAST_ID_ERROR_PUT_CACHE_CONFIGS,
      'error',
      errMsg as string)
  }
}

const handleGetCacheKeys = async (isReload = false) => {
  isDownloading.value = true
  // fetch data
  try {
    const response = await api.getCacheKeys()
    utils.validateResponse(response)
    // handle success
    cacheKeys.value = response.data.keys
    await utils.sleep(150)
    isDownloading.value = false
    if (!isReload) {
      blinkToast(
        TOAST_ID_SUCCESS_GET_CACHE_KEYS,
        'info',
        MSG_SUCCESS_GET_CACHE_KEYS)
    }
  }
  catch (errMsg) {
    // handle error
    cacheKeys.value = []
    blinkToast(
      TOAST_ID_ERROR_GET_CACHE_KEYS,
      'error',
      errMsg as string)
    isDownloading.value = false
  }
}

const handleDeleteCache = async () => {
  // fetch data
  try {
    const response = await api.postClearCache()
    utils.validateResponse(response)
    // handle success
    blinkToast(
      TOAST_ID_SUCCESS_CLEAR_CACHE,
      'success',
      MSG_SUCCESS_CLEAR_CACHE)
    await handleGetCacheKeys(true)
  }
  catch (errMsg) {
    // handle error
    blinkToast(
      TOAST_ID_ERROR_CLEAR_CACHE,
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
  <h1 my-title-style>
    Config
  </h1>

  <!-- Page Content -->
  <ThePageContent>
    <!-- Input Group -->
    <TheInputGroup
      w-xs
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
          my-input-style
        >
          <option disabled>
            Choose one of the following:
          </option>
          <option value="random">
            Least Recently Used
          </option>
          <option value="LRU">
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
            my-input-style
            placeholder="Enter a number"
          >
          <span
            inline-flex items-center px-3
            my-border rounded-l-none border-l-0
            my-input-style
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
        :modal-id="MODAL_ID_PUT_CACHE_CONFIGS"
        modal-type="submit"
        :modal-title="MODAL_TITLE_PUT_CACHE_CONFIGS"
        :modal-description="MODAL_DESCRIPTION_PUT_CACHE_CONFIGS(cacheConfigs.replacementPolicy, cacheConfigs.maxSize)"
        :action="handlePutCacheConfigs"
      />
    </TheInputGroup>

    <!-- HR -->
    <TheConfigHR />

    <!-- Table: All Keys -->
    <TheKeyTable
      :data="cacheKeys"
      :table-title="TABLE_TITLE_CACHE_KEYS"
      :table-description="TABLE_DESCRIPTION_CACHE_KEYS"
      :delete-button-text="TABLE_DELETE_BUTTON_TEXT_CACHE_KEYS"
      :delete-button-action="handleDeleteCache"
      :modal-id="MODAL_ID_CLEAR_CACHE"
      :modal-title="MODAL_TITLE_CLEAR_CACHE"
      :modal-description="MODAL_DESCRIPTION_CLEAR_CACHE"
      :class="{ 'blur-sm grayscale': isDownloading }"
      transition-all duration-300
    />
  </ThePageContent>

  <!-- Toasts, Alerts & Modals -->
  <TheToasts
    :toasts-array="toastsArray"
  />
</template>
