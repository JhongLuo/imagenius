<script setup lang="ts">
defineOptions({
  name: 'RetrievePage',
})

const api = useAPIStore()
const { toastsArray, blinkToast } = useToasts()

const imgKey = ref('')
const imgStr = ref('')
const isDownloading = ref(false)
const lastKey = ref('')

const isInputValid = computed(() => imgKey.value)

const handleRetrieve = async () => {
  // input validation
  if (!isInputValid.value)
    return

  // start retrieval
  isDownloading.value = true
  // fetch data
  try {
    const key = imgKey.value
    const response = await api.getImage(key)
    utils.validateResponse(response)
    // handle success
    // update lastKey + img src, show blurred img
    await utils.sleep(50)
    lastKey.value = key
    imgStr.value = response.data.content
    // unblur img and show toast
    await utils.sleep(50)
    isDownloading.value = false
    blinkToast(
      TOAST_ID_SUCCESS_RETRIEVE_IMG,
      'success',
      MSG_SUCCESS_RETRIEVE_IMG)
  }
  catch (errMsg) {
    // handle error
    imgStr.value = ''
    blinkToast(
      TOAST_ID_ERROR_RETRIEVE_IMG,
      'error',
      errMsg as string)
    isDownloading.value = false
  }
}
</script>

<template>
  <!-- Page Title -->
  <h1 my-title-style>
    Retrieve
  </h1>

  <!-- Page Content -->
  <ThePageContent>
    <!-- Input group: -->
    <div
      w-full
      flex flex-row justify-between items-end
    >
      <!-- input: image key -->
      <div
        class="w-61.8%"
      >
        <TheLabeledInput
          input-id="input-image-key"
          label-text="Image Key"
        >
          <TheIconedTextInput
            v-model.trim="imgKey"
            icon="i-carbon-password"
            input-id="input-image-key"
            placeholder="Your image key"
            @keydown.enter="handleRetrieve"
          />
        </TheLabeledInput>
      </div>

      <!-- Group <upload button + spinner> -->
      <div
        flex items-center space-x-3
      >
        <!-- spinner -->
        <TheSpinner
          v-if="isDownloading"
          alt-text="Downloading..."
        />

        <!-- button: retrieve -->
        <TheButton
          label="Get"
          :disabled="!isInputValid"
          @click="handleRetrieve"
        />
      </div>
    </div>

    <!-- Image Preview: -->
    <TheImagePreview
      :src="imgStr"
      caption-pos="top-right"
      :caption-text="isDownloading ? 'Requesting...' : `Image <${lastKey}>`"
      alt="Resulteview: Retrieved Image"
      :class="{ 'blur-sm grayscale': isDownloading }"
      transition-all duration-300
    />
  </ThePageContent>

  <!-- Toasts, Alerts & Modals -->
  <TheToasts
    :toasts-array="toastsArray"
  />
</template>
