<script setup lang="ts">
import type { Image, RawImageData, Selectable } from '~/composables/utils'

defineOptions({
  name: 'AddPage',
})

const api = useAPIStore()
const { toastsArray, blinkToast } = useToasts()

const generatePrompt = ref<string>('')
const imgsGenerated = ref<(Image & Selectable)[]>([])
const jokeGenerated = ref<string>('')
const numImgsResult = ref<number>(0)
const imgsSelected = computed<(Image & Selectable)[]>(() => imgsGenerated.value.filter(img => img.selected))

const isGenerating = ref<boolean>(false)
const isSaving = ref<boolean>(false)
const numOfTimesTitleClicked = ref<number>(0)

const isPromptValid = computed<boolean>(() => generatePrompt.value.length > 0)
const isSelectionValid = computed<boolean>(() => imgsSelected.value.length > 0)

let wasPromptFromHint = false
const isShownHint = ref<boolean>(true)

watch(generatePrompt, (newVal: string) => {
  isShownHint.value = !(newVal.length > 0 && !wasPromptFromHint)
  wasPromptFromHint = false
})

const handleGenerateHint = async () => {
  try {
    const response = await api.generateRandomWord()
    utilsJS.validateResponse(response)
    // handle success
    const randomWord = response.data.word
    wasPromptFromHint = true
    generatePrompt.value = randomWord
  }
  catch (err) {
    // handle error
    blinkToast(
      TOAST_ID__GENERATE_HINT__ERROR,
      'error',
      err as string)
  }
}

const handleGenerate = async () => {
  // input validation
  if (!isPromptValid.value)
    return

  // start generate
  isGenerating.value = true
  try {
    // construct request form data
    const fd = new FormData()
    fd.append('prompt', generatePrompt.value.trim())
    const response = await api.generateImages(fd)
    utilsJS.validateResponse(response)
    // handle success
    const rawDatas: RawImageData[] = response.data.images
    imgsGenerated.value = rawDatas.map((rawData: RawImageData) => ({
      key: rawData.key,
      src: '',
      srcSaved: rawData.src,
      selected: false,
    } as Image & Selectable))
    numImgsResult.value = imgsGenerated.value.length
    // finish loading and start display
    await utils.sleep(50)
    isGenerating.value = false
    imgsGenerated.value.forEach((img: (Image & Selectable)) => {
      img.src = img.srcSaved
    })
    jokeGenerated.value = response.data.joke
    blinkToast(
      TOAST_ID__GENERATE_IMGS__SUCCESS,
      'success',
      TOAST_MSG__GENERATE_IMGS__SUCCESS)
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
    fd.append('selected_keys', JSON.stringify(selectedKeys))
    const response = await api.saveImages(fd)
    utilsJS.validateResponse(response)
    // handle success
    // start displaying results
    await utils.sleep(50)
    generatePrompt.value = ''
    imgsGenerated.value.forEach((img: (Image & Selectable)) => {
      img.src = ''
    })
    // clear displayed results
    await utils.sleep(50)
    imgsGenerated.value = []
    jokeGenerated.value = ''
    isSaving.value = false
    blinkToast(
      TOAST_ID__SAVE_IMGS__SUCCESS,
      'success',
      TOAST_MSG__SAVE_IMGS__SUCCESS)
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
  <h1
    my-title
    @click="numOfTimesTitleClicked++"
  >
    Add New
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
            v-model="generatePrompt"
            icon="i-carbon:ibm-watson-speech-to-text"
            input-id="input-image-prompt"
            placeholder="Prompt for generating images..."
            @keydown.enter="handleGenerate"
          />
        </TheLabeledInput>
      </div>

      <!-- Group <generate button + spinner> -->
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
          :disabled="!isPromptValid || isGenerating"
          @click="handleGenerate"
        />
      </div>
    </div>

    <!-- Random prompt word -->
    <div
      w-full
      ms-1 mb-4
      text-start
    >
      <a
        v-if="isShownHint"
        text-xs text-teal-600 hover:text-teal-500 hover:underline cursor-pointer
        @click="handleGenerateHint"
      >
        No ideas? Click here for something to begin with.
      </a>
    </div>

    <!-- Select and Submission: -->
    <div
      mt-8
      grid gap-4
      :class="{
        'grid-cols-1': numImgsResult === 1,
        'grid-cols-2': numImgsResult >= 2,
      }"
    >
      <TheImagePreview
        v-for="img in imgsGenerated"
        :key="img.key"
        :src="img.src"
        caption-pos="bottom-right"
        :caption-text="img.selected ? '✓' : ''"
        :alt="img.key"
        :class="{ 'blur-sm grayscale': isGenerating || isSaving }"
        transition-all duration-300
        @click="img.selected = !img.selected"
      />
    </div>

    <!-- Group <save button + spinner> -->
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
        :disabled="!isSelectionValid || isSaving"
        @click="handleSave"
      />
    </div>

    <div
      v-if="jokeGenerated.length > 0 && numOfTimesTitleClicked >= 3"
      border
      mt-8 p-4
      w-md rounded-lg
    >
      🤣 A bonus joke: 🤣
      <br>
      <br>
      {{ jokeGenerated }}
    </div>
  </ThePageContent>

  <!-- Toasts, Alerts & Modals -->
  <TheToasts
    :toasts-array="toastsArray"
  />
</template>
