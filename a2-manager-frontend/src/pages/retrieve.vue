<script setup lang="ts">
defineOptions({
  name: 'RetrievePage',
})

const api = useAPIStore()
const { toastsArray, blinkToast } = useToasts()

const imgKey = ref('')
const imgStr = ref('')
const isDownloading = ref(false)

const isInputValid = computed(() => imgKey.value.trim())

const handleRetrieve = async () => {
  // < input validation already done by button disabled state >
  isDownloading.value = true
  // fetch data
  try {
    const key = imgKey.value.trim()
    const response = await api.getImage(key)
    utils.validateResponse(response)
    // handle success
    setTimeout(() => {
      imgStr.value = response.data.content
    }, 100)
    setTimeout(() => {
      isDownloading.value = false
      blinkToast('toast-image-retrieve-success', 'success', 'Image retrieved successfully.')
    }, 100)
  }
  catch (errMsg) {
    // handle error
    imgStr.value = ''
    blinkToast('toast-image-retrieve-error', 'error', errMsg as string)
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
  <div
    w-sm
    flex flex-col items-center
  >
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
            v-model="imgKey"
            icon="i-carbon-password"
            input-id="input-image-key"
            placeholder="Your image key"
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
      :class="{ 'blur-sm grayscale': isDownloading }"
      caption-pos="top-right"
      :caption-text="isDownloading ? 'Downloading...' : 'Image Result'"
      alt="Resulteview: Retrieved Image"
    />
  </div>

  <!-- Toasts, Alerts & Modals -->
  <TheToasts
    :toasts-array="toastsArray"
  />
</template>
