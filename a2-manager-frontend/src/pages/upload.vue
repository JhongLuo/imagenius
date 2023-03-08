<script setup lang="ts">
defineOptions({
  name: 'UploadPage',
})

const api = useAPIStore()
const { imgStr, updateImgFile } = useImageUpload()
const { toastsArray, blinkToast } = useToasts()

const imgKey = ref('')
const isUploading = ref(false)

const onFileInputChanged = (event: Event) => {
  updateImgFile(event)
}

const isInputValid = computed(() => imgKey.value && imgStr.value)

const handleUpload = async () => {
  // < input validation already done by button disabled state >
  isUploading.value = true
  // fetch data
  try {
    // construct request form data
    const fd = new FormData()
    fd.append('key', imgKey.value)
    fd.append('file', imgStr.value)
    const response = await api.postImage(fd)
    utils.validateResponse(response)
    // handle success
    blinkToast(
      TOAST_ID_SUCCESS_UPLOAD_IMG,
      'success',
      MSG_SUCCESS_UPLOAD_IMG)
    isUploading.value = false
    imgKey.value = ''
    imgStr.value = '';
    (document.getElementById('input-image-file')! as HTMLInputElement).value = ''
  }
  catch (errMsg) {
    // handle error
    blinkToast(
      TOAST_ID_ERROR_UPLOAD_IMG,
      'error',
      errMsg as string)
    isUploading.value = false
  }
}
</script>

<template>
  <!-- Page Title -->
  <h1 my-title-style>
    Upload
  </h1>

  <!-- Page Content -->
  <ThePageContent>
    <!-- Input group: -->
    <div
      w-full
      flex flex-col items-start
    >
      <!-- input: image key -->
      <div
        class="w-61.8%"
        mb-4
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
          />
        </TheLabeledInput>
      </div>

      <!-- input: image file -->
      <TheFileInput
        accept="image/*"
        label-text="Image File"
        input-id="input-image-file"
        helper-text-id="input-image-file-help"
        helper-text="Image format only (e.g. PNG, JPG, GIF, etc.)"
        @change="onFileInputChanged"
      />

      <!-- Group <upload button + spinner> -->
      <div
        mt-5
        flex items-center space-x-3
      >
        <!-- button: upload -->
        <TheButton
          label="Upload"
          :disabled="!isInputValid"
          @click="handleUpload"
        />

        <!-- spinner -->
        <TheSpinner
          v-if="isUploading"
          alt-text="Uploading..."
        />
      </div>
    </div>

    <!-- Image Preview: -->
    <TheImagePreview
      :src="imgStr"
      caption-pos="top-right"
      :caption-text="isUploading ? 'Uploading...' : 'Image Preview'"
      alt="Preview: Image To Be Uploaded"
      :class="{ 'blur-sm grayscale': isUploading }"
      transition-all duration-300
    />
  </ThePageContent>

  <!-- Toasts, Alerts & Modals -->
  <TheToasts
    :toasts-array="toastsArray"
  />
</template>
