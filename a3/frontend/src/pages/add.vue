<script setup lang="ts">
defineOptions({
  name: 'AddPage',
})

const api = useAPIStore()
const { toastsArray, blinkToast } = useToasts()

const generatePrompt = ref('')
const imgsGenerated = ref<ImageGenerated[]>([])
const imgsSelected = computed<ImageGenerated[]>(() => imgsGenerated.value.filter(img => img.selected))

const isGenerating = ref(false)
const isSaving = ref(false)

const isPromptValid = computed(() => generatePrompt.value)
const isSelectionValid = computed(() => imgsSelected.value.length > 0)

const handleGenerate = async () => {
  // input validation
  if (!isPromptValid.value)
    return

  // start generate
  isGenerating.value = true
  try {
    // construct request form data
    const fd = new FormData()
    fd.append('prompt', generatePrompt.value)
    const response = await api.generateImages(fd)
    utilsJS.validateResponse(response)
    // handle success
    await utils.sleep(50)
    imgsGenerated.value = []
    response.data.images.forEach((imgData: RawImageData) => {
      imgsGenerated.value.push({
        key: imgData.key,
        src: imgData.src,
        selected: false,
      } as ImageGenerated)
    })
    blinkToast(
      TOAST_ID__GENERATE_IMGS__SUCCESS,
      'success',
      TOAST_MSG__GENERATE_IMGS__SUCCESS)
    isGenerating.value = false
  }
  catch (err) {
    // handle error
    blinkToast(
      TOAST_ID__GENERATE_IMGS__ERROR,
      'error',
      err as string)
    isGenerating.value = false
  }
}

const handleSave = async () => {
  // input validation
  if (!isSelectionValid.value)
    return

  // start generate
  isSaving.value = true
  try {
    // construct request form data
    const fd = new FormData()
    const selectedKeys = imgsSelected.value.map(img => img.key)
    fd.append('key_selections', JSON.stringify(selectedKeys))
    const response = await api.saveImages(fd)
    utilsJS.validateResponse(response)
    // handle success
    await utils.sleep(50)
    imgsGenerated.value = []
    generatePrompt.value = ''
    blinkToast(
      TOAST_ID__SAVE_IMGS__SUCCESS,
      'success',
      TOAST_MSG__SAVE_IMGS__SUCCESS)
    isSaving.value = false
  }
  catch (err) {
    // handle error
    blinkToast(
      TOAST_ID__SAVE_IMGS__ERROR,
      'error',
      err as string)
    isSaving.value = false
  }
}
</script>

<template>
  <!-- Page Title -->
  <h1 my-title>
    Add
  </h1>

  <!-- Page Content -->
  <ThePageContent>
    <!-- Input group: -->
    <div
      w-full
      flex flex-row justify-between items-end
    >
      <!-- input: generate prompt -->
      <div
        class="w-65%"
      >
        <TheLabeledInput
          input-id="input-generate-prompt"
          label-text="Image Generation Prompt"
        >
          <TheIconedTextInput
            v-model.trim="generatePrompt"
            icon="i-carbon:ibm-watson-speech-to-text"
            input-id="input-image-prompt"
            placeholder="Prompt for generating images..."
            @keydown.enter="handleGenerate"
          />
        </TheLabeledInput>
      </div>

      <!-- Group <upload button + spinner> -->
      <div
        flex items-center space-x-3
      >
        <!-- spinner -->
        <TheSpinner
          v-if="isGenerating"
          alt-text="Generating..."
        />

        <!-- button: retrieve -->
        <TheButton
          :label="imgsGenerated.length ? 'Regenerate' : 'Generate'"
          :disabled="!isPromptValid"
          @click="handleGenerate"
        />
      </div>
    </div>

    <!-- Select and Submission: -->
    <div
      w-full h-full
      mt-8
      grid grid-cols-2 gap-4
    >
      <TheImagePreview
        v-for="img in imgsGenerated"
        :key="img.key"
        :src="img.src"
        caption-pos="bottom-right"
        :caption-text="img.selected ? '✓' : ''"
        :alt="img.key"
        :class="{ 'blur-sm grayscale': isSaving }"
        transition-all
        duration-300
        @click="img.selected = !img.selected"
      />
    </div>

    <!-- Group <upload button + spinner> -->
    <div
      v-if="imgsGenerated.length"
      mt-8
      flex items-center space-x-3
    >
      <!-- spinner -->
      <TheSpinner
        v-if="isSaving"
        alt-text="Saving..."
      />

      <!-- button: retrieve -->
      <TheButton
        label="Save"
        :disabled="!isSelectionValid"
        @click="handleSave"
      />
    </div>
  </ThePageContent>

  <!-- Toasts, Alerts & Modals -->
  <TheToasts
    :toasts-array="toastsArray"
  />
</template>
