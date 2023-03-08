<script setup lang="ts">
defineOptions({
  name: 'UploadPage',
})

const api = useAPIStore()
const { imgStr, updateImgFile } = useImageUpload()
const imgKey = ref('')
const isUploading = ref(false)
const isUploaded = ref(false)

const isInputValid = computed(() => {
  return imgKey.value.trim() && imgStr.value
})

const onFileInputChanged = (event: Event) => {
  isUploaded.value = false
  updateImgFile(event)
}

const handleUpload = async () => {
  // TODO: complete this
  // <== input validation already done by button disabled state
  isUploading.value = true
  // fetch data
  try {
    // construct request form data
    const fd = new FormData()
    fd.append('key', imgKey.value.trim())
    fd.append('file', imgStr.value)
    const response = await api.postImage(fd)
    utils.helperThrowIfNotSuccess(response)
    // handle success
    isUploaded.value = true
    // reset states
    isUploading.value = false
    imgKey.value = ''
    // imgStr.value = ''
  }
  catch (errMsg) {
    // handle error
    console.error(errMsg)
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
    <form
      w-full
      flex flex-col items-start
      @submit.prevent
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
    </form>

    <!-- Image Preview: -->
    <TheImagePreview
      v-if="imgStr"
      :src="imgStr"
      :class="{ 'blur-sm': isUploaded }"
      :caption-show="!isUploaded"
      caption-pos="top-right"
      caption-text="Image Preview"
      alt="Preview: Image To Be Uploaded"
    />
  </div>
</template>
