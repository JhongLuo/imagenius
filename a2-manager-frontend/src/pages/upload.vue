<script setup lang="ts">
const api = useAPIStore()
const { imgStr, updateImgFile } = useImageUpload()

const imgKey = ref('')
const isUploading = ref(false)
const isShownToastSuccess = ref(false)
const isShownToastError = ref(false)
const uploadErrorMsg = ref('')

const onFileInputChanged = (event: Event) => {
  updateImgFile(event)
}

const isInputValid = computed(() => {
  return imgKey.value.trim() && imgStr.value
})

const popToast = (toastSelection: string) => {
  // bind toast selection
  const setToastShownStatus = (status: boolean) => {
    if (toastSelection === 'success')
      isShownToastSuccess.value = status
    else if (toastSelection === 'error')
      isShownToastError.value = status
  }

  // show toast
  setToastShownStatus(true)

  // hide toast after 3 seconds
  return new Promise((resolve) => {
    setTimeout(() => {
      setToastShownStatus(false)
      resolve('')
    }, 4000)
  })
}

const handleUpload = async () => {
  // < input validation already done by button disabled state >
  isUploading.value = true
  // fetch data
  try {
    // construct request form data
    const fd = new FormData()
    fd.append('key', imgKey.value.trim())
    fd.append('file', imgStr.value)
    const response = await api.postImage(fd)
    utils.validateResponse(response)
    // handle success
    popToast('success')
    isUploading.value = false
    imgKey.value = ''
    imgStr.value = '';
    (document.getElementById('input-image-file')! as HTMLInputElement).value = ''
  }
  catch (errMsg) {
    // handle error
    uploadErrorMsg.value = errMsg as string
    popToast('error')
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
  <div
    w-sm
    flex flex-col items-center
  >
    <!-- Input group: -->
    <div
      w-full
      flex flex-col items-start
    >
      <!-- input: image key  -->
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

      <!-- input: image file -->
      <TheFileInput
        accept="image/*"
        label-text="Image File"
        input-id="input-image-file"
        helper-text-id="input-image-file-help"
        helper-text="Image format only (e.g. PNG, JPG, GIF, etc.)"
        @change="onFileInputChanged"
      />

      <!-- Button + Spinner -->
      <div mt-5 flex items-center space-x-3>
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
    <Transition>
      <TheImagePreview
        :src="imgStr"
        :class="{ 'blur-sm grayscale': isUploading }"
        caption-pos="top-right"
        :caption-text="isUploading ? 'Uploading...' : 'Image Preview'"
        alt="Preview: Image To Be Uploaded"
      />
    </Transition>
  </div>

  <!-- Toasts, Alerts & Modals -->
  <TheToastContainer>
    <TheToast
      v-model="isShownToastSuccess"
      toast-id="toast-success"
      toast-type="success"
      toast-text="Image was uploaded successfully."
    />
    <TheToast
      v-model="isShownToastError"
      toast-id="toast-error"
      toast-type="error"
      :toast-text="uploadErrorMsg"
    />
  </TheToastContainer>
</template>
