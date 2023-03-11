<script setup lang="ts">
defineOptions({
  name: 'ConfigPage',
})

const api = useAPIStore()
const { toastsArray, blinkToast } = useToasts()

const cacheConfigs = reactive<CacheConfigOptions>({
  mode: 'auto',
  numNodes: -1,
  cacheSize: 0,
  policy: 'LRU',
  expRatio: 1,
  shrinkRatio: 1,
  maxMiss: 0,
  minMiss: 0,
})

const cacheKeys = ref([])
const isDownloadingCacheConfigs = ref(false)
const isDownloadingCacheKeys = ref(false)
const isModalPutCacheConfigsShown = ref(false)

const cacheOptionsValidity = computed(() => {
  return {
    cacheSize: cacheConfigs.cacheSize !== '' && cacheConfigs.cacheSize >= 0,
    expRatio: cacheConfigs.expRatio !== '' && cacheConfigs.expRatio >= 1,
    shrinkRatio: cacheConfigs.shrinkRatio !== '' && cacheConfigs.shrinkRatio >= 0 && cacheConfigs.shrinkRatio <= 1,
  }
})

const isFormValid = computed(() => {
  if (!cacheOptionsValidity.value.cacheSize)
    return false

  if (cacheConfigs.mode === 'auto') { // manual
    return cacheOptionsValidity.value.expRatio && cacheOptionsValidity.value.shrinkRatio
  }

  else {
    return true
  }
})

const handleGetCacheConfigs = async (isReload = false) => {
  isDownloadingCacheConfigs.value = true
  // fetch data
  try {
    const response = await api.getCacheConfigsNew()
    utilsJS.validateResponse(response)
    // handle success
    cacheConfigs.mode = response.data.mode
    cacheConfigs.numNodes = response.data.numNodes
    cacheConfigs.cacheSize = response.data.cacheSize
    cacheConfigs.policy = response.data.policy
    cacheConfigs.expRatio = response.data.expRatio
    cacheConfigs.shrinkRatio = response.data.shrinkRatio
    cacheConfigs.maxMiss = response.data.maxMiss * 100
    cacheConfigs.minMiss = response.data.minMiss * 100
    await utils.sleep(150)
    isDownloadingCacheConfigs.value = false
    if (!isReload) {
      blinkToast(
        TOAST_ID__GET_CACHE_CONFIGS__SUCCESS,
        'info',
        TOAST_MSG__GET_CACHE_CONFIGS__SUCCESS)
    }
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
      mode: cacheConfigs.mode,
      numNodes: (cacheConfigs.mode === 'manual' && typeof cacheConfigs.numNodes === 'number') ? cacheConfigs.numNodes : undefined,
      cacheSize: cacheConfigs.cacheSize,
      policy: cacheConfigs.policy,
      expRatio: (cacheConfigs.mode === 'auto' && typeof cacheConfigs.expRatio === 'number') ? cacheConfigs.expRatio : undefined,
      shrinkRatio: (cacheConfigs.mode === 'auto' && typeof cacheConfigs.shrinkRatio === 'number') ? cacheConfigs.shrinkRatio : undefined,
      maxMiss: (cacheConfigs.mode === 'auto' && typeof cacheConfigs.maxMiss === 'number') ? cacheConfigs.maxMiss / 100 : undefined,
      minMiss: (cacheConfigs.mode === 'auto' && typeof cacheConfigs.minMiss === 'number') ? cacheConfigs.minMiss / 100 : undefined,
    } as CacheConfigOptions
    const response = await api.putCacheConfigsNew(data)
    utilsJS.validateResponse(response)
    // handle success
    blinkToast(
      TOAST_ID__PUT_CACHE_CONFIGS__SUCCESS,
      'success',
      TOAST_MSG__PUT_CACHE_CONFIGS__SUCCESS)
    await handleGetCacheConfigs(true)
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
  isDownloadingCacheKeys.value = true
  // fetch data
  try {
    const response = await api.getCacheKeys()
    utilsJS.validateResponse(response)
    // handle success
    cacheKeys.value = response.data.keys
    await utils.sleep(150)
    isDownloadingCacheKeys.value = false
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
  initTooltips()
  handleGetCacheConfigs()
  handleGetCacheKeys()
})
</script>

<template>
  <!-- Page Title -->
  <h1 my-title>
    Cache Config
  </h1>

  <!-- Page Content -->
  <ThePageContent>
    <div
      :class="{
        'blur-sm grayscale': isDownloadingCacheConfigs,
        'invisible': cacheConfigs.numNodes === -1,
      }"
      transition-all duration-300
    >
      <!-- Input Group -->
      <TheInputGroup
        w-xs
        px-8 py-6
        my-bg-secondary
        my-card my-shadow-light
      >
        <!-- Mode: manual / auto -->
        <TheLabeledInput
          input-id="input-manual-auto-mode"
          label-text="Mode"
          mb-3
        >
          <select
            id="input-manual-auto-mode"
            v-model="cacheConfigs.mode"
            w-full p-2.5
            text-sm my-text-color-primary
            my-input
          >
            <option disabled>
              Choose one of the following:
            </option>
            <option value="manual">
              Manual
            </option>
            <option value="auto">
              Auto
            </option>
          </select>
        </TheLabeledInput>

        <!-- Num Nodes: Manual Change -->
        <TheLabeledInput
          input-id="input-num-nodes"
          label-text="# of Nodes"
        >
          <input
            id="input-num-nodes"
            v-model="cacheConfigs.numNodes"
            type="number"
            min="1"
            max="8"
            step="1"
            class="w-61.8%"
            flex-grow-1
            my-border
            my-input disabled:pointer-events-none
            data-tooltip-target="tooltip-num-nodes"
            placeholder="<empty>"
            onkeydown="return false"
            :disabled="cacheConfigs.mode !== 'manual'"
          >

          <TheTooltip
            id="tooltip-num-nodes"
            label="1 <= Value <= 8"
          />

          <TheInputHelperText
            helper-text="Manual mode only."
          />
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
              v-model="cacheConfigs.cacheSize"
              type="number"
              min="0"
              flex-grow-1
              my-border rounded-r-none
              my-input
              data-tooltip-target="tooltip-cache-size"
              placeholder="<empty>"
            >
            <span
              inline-flex items-center px-3
              my-border rounded-l-none border-l-0
              my-input select-none
            >
              MB
            </span>
          </div>

          <TheTooltip
            id="tooltip-cache-size"
            label="Value ≥ 0"
          />
        </TheLabeledInput>

        <!-- Replacement Policy -->
        <TheLabeledInput
          input-id="input-replacement-policy"
          label-text="Replacement Policy"
          mb-3
        >
          <select
            id="input-replacement-policy"
            v-model="cacheConfigs.policy"
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
            <option value="RR">
              Random Replacement
            </option>
          </select>
        </TheLabeledInput>

        <!-- Expand / Shrink Ratio -->
        <TheLabeledInput
          input-id="input-ratio"
          label-text="Expand/Shrink Ratio"
        >
          <!-- row -->
          <div
            flex justify-between w-full
          >
            <!-- col: expRatio -->
            <div
              class="w-45%"
              flex flex-col items-center
            >
              <input
                id="input-ratio-expand"
                v-model="cacheConfigs.expRatio"
                type="number"
                w-full h-full
                my-border
                my-input text-center
                placeholder="<empty>"
                :disabled="cacheConfigs.mode !== 'auto'"
              >

              <TheInputHelperText
                helper-text="Expand Ratio ≥ 1"
              />
            </div>
            <!-- col: shrinkRatio -->
            <div
              class="w-45%"
              flex flex-col items-center
            >
              <input
                id="input-ratio-shrink"
                v-model="cacheConfigs.shrinkRatio"
                type="number"
                w-full h-full
                my-border
                my-input text-center
                placeholder="<empty>"
                :disabled="cacheConfigs.mode !== 'auto'"
              >

              <TheInputHelperText
                helper-text="0 ≤ Shrink Ratio ≤ 1"
              />
            </div>
          </div>
        </TheLabeledInput>

        <!-- Max / Min Miss -->
        <TheLabeledInput
          input-id="input-miss-rate"
          label-text="Max/Min Miss Rate"
        >
          <!-- row -->
          <div
            flex justify-between w-full
          >
            <!-- col: maxMiss -->
            <div
              class="w-45%"
              flex flex-col items-center
            >
              <div
                flex w-full
              >
                <input
                  id="input-miss-rate-max"
                  v-model="cacheConfigs.maxMiss"
                  type="number"
                  oninput="this.value = this.value > 100 ? 100 : Math.floor(this.value)"
                  w-full h-full
                  my-border rounded-r-none
                  my-input text-center
                  data-tooltip-target="tooltip-max-miss"
                  placeholder="<empty>"
                  :disabled="cacheConfigs.mode !== 'auto'"
                >
                <span
                  inline-flex items-center px-3
                  my-border rounded-l-none border-l-0
                  my-input select-none
                >
                  %
                </span>
              </div>

              <TheTooltip
                id="tooltip-max-miss"
                label="Interger Only"
              />

              <TheInputHelperText
                helper-text="Max Miss Rate"
              />
            </div>
            <!-- col: minMiss -->
            <div
              class="w-45%"
              flex flex-col items-center
            >
              <div
                flex w-full
              >
                <input
                  id="input-miss-rate-min"
                  v-model="cacheConfigs.minMiss"
                  type="number"
                  oninput="this.value = this.value > 100 ? 100 : Math.floor(this.value)"
                  w-full h-full
                  my-border rounded-r-none
                  my-input text-center
                  data-tooltip-target="tooltip-min-miss"
                  placeholder="<empty>"
                  :disabled="cacheConfigs.mode !== 'auto'"
                >
                <span
                  inline-flex items-center px-3
                  my-border rounded-l-none border-l-0
                  my-input select-none
                >
                  %
                </span>
              </div>

              <TheTooltip
                id="tooltip-min-miss"
                label="Integers Only"
              />

              <TheInputHelperText
                helper-text="Min Miss Rate"
              />
            </div>
          </div>
        </TheLabeledInput>

        <!-- Button: Submit New Cache Configs -->
        <TheButton
          text-sm
          label="Update"
          :disabled="!isFormValid"
          @click="isModalPutCacheConfigsShown = true"
        />

        <!-- Modal: Put Cache Configs -->
        <TheModal
          v-model:is-shown="isModalPutCacheConfigsShown"
          modal-type="submit"
          :modal-id="MODAL_ID__PUT_CACHE_CONFIGS"
          :modal-title="MODAL_TITLE__PUT_CACHE_CONFIGS"
          :modal-description="MODAL_DESCRIPTION__PUT_CACHE_CONFIGS({
            mode: cacheConfigs.mode,
            numNodes: cacheConfigs.numNodes,
            cacheSize: cacheConfigs.cacheSize,
            policy: cacheConfigs.policy,
            expRatio: cacheConfigs.expRatio,
            shrinkRatio: cacheConfigs.shrinkRatio,
            maxMiss: cacheConfigs.maxMiss,
            minMiss: cacheConfigs.minMiss,
          } as CacheConfigOptions)"
          :action="handlePutCacheConfigs"
        />
      </TheInputGroup>
    </div>

    <!-- HR -->
    <TheConfigHR />

    <!-- Table: Cache Keys -->
    <TheKeyTable
      :data="cacheKeys"
      :table-title="TABLE_TITLE__CACHE_KEYS"
      :table-description="TABLE_DESCRIPTION__CACHE_KEYS"
      :delete-button-text="TABLE_DELETE_BUTTON_TEXT__CACHE_KEYS"
      :delete-button-action="handleDeleteCache"
      :modal-id="MODAL_ID__CLEAR_CACHE"
      :modal-title="MODAL_TITLE__CLEAR_CACHE"
      :modal-description="MODAL_DESCRIPTION__CLEAR_CACHE"
      :class="{ 'blur-sm grayscale': isDownloadingCacheKeys }"
      transition-all duration-300
    />
  </ThePageContent>

  <!-- Toasts, Alerts & Modals -->
  <TheToasts
    :toasts-array="toastsArray"
  />
</template>

<style scoped>
#input-max-cache-size::-webkit-outer-spin-button,
#input-ratio-expand::-webkit-outer-spin-button,
#input-ratio-shrink::-webkit-outer-spin-button,
#input-max-cache-size::-webkit-inner-spin-button,
#input-ratio-expand::-webkit-inner-spin-button,
#input-ratio-shrink::-webkit-inner-spin-button,
#input-miss-rate-max::-webkit-inner-spin-button,
#input-miss-rate-min::-webkit-inner-spin-button
{
  -webkit-appearance: none;
    margin: 0;
}

#input-max-cache-size,
#input-ratio-expand,
#input-ratio-shrink,
#input-miss-rate-max,
#input-miss-rate-min
{
  -moz-appearance: textfield;
}
</style>
