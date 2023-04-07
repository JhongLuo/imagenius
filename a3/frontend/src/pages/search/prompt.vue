<script setup lang="ts">
import type { Image, RawImageData } from '~/composables/utils'

defineOptions({
  name: 'SearchByPromptPage',
})

const api = useAPIStore()
const { toastsArray, blinkToast } = useToasts()

const searchPrompt = ref('')
const imgsSearchResult = ref<Image[]>([])

const isSearching = ref(false)

const isPromptValid = computed(() => searchPrompt.value)

const handleSearchByPrompt = async () => {
  // input validation
  if (!isPromptValid.value)
    return

  // start generate
  isSearching.value = true
  try {
    // construct request form data
    const fd = new FormData()
    fd.append('prompt', searchPrompt.value)
    const response = await api.searchImagesByPrompt(fd)
    utilsJS.validateResponse(response)
    // handle success
    imgsSearchResult.value = []
    response.data.images.forEach((imgData: RawImageData) => {
      imgsSearchResult.value.push({
        key: imgData.key,
        src: '',
        srcSaved: imgData.src,
      } as Image)
    })
    // finish loading and start displaying results
    await utils.sleep(50)
    isSearching.value = false
    imgsSearchResult.value.forEach((img: Image) => {
      img.src = img.srcSaved
    })
    blinkToast(
      TOAST_ID__SEARCH_IMGS__SUCCESS,
      'success',
      TOAST_MSG__SEARCH_IMGS__SUCCESS)
  }
  catch (err) {
    // handle error
    blinkToast(
      TOAST_ID__SEARCH_IMGS__ERROR,
      'error',
      err as string)
    isSearching.value = false
  }
}
</script>

<template>
  <!-- Page Title -->
  <h1 my-title>
    Search By Prompt
  </h1>

  <!-- Page Content -->
  <ThePageContent>
    <!-- Input group: -->
    <div
      w-full
      flex flex-row justify-between items-end
    >
      <!-- input: search prompt -->
      <div
        class="w-65%"
      >
        <TheLabeledInput
          input-id="input-image-key"
          label-text="Image Search Prompt"
        >
          <TheIconedTextInput
            v-model.trim="searchPrompt"
            icon="i-carbon:ibm-watson-speech-to-text"
            input-id="input-image-prompt"
            placeholder="Prompt for image search..."
            @keydown.enter="handleSearchByPrompt"
          />
        </TheLabeledInput>
      </div>

      <!-- Group <search button + spinner> -->
      <div
        flex items-center space-x-3
      >
        <!-- spinner -->
        <TheSpinner
          v-if="isSearching"
          alt-text="Generating..."
        />

        <!-- button: retrieve -->
        <TheButton
          label="Search"
          :disabled="!isPromptValid"
          @click="handleSearchByPrompt"
        />
      </div>
    </div>

    <!-- Search Results: -->
    <div
      w-full h-full
      mt-8
      grid gap-4
      :class="{
        'grid-cols-1': imgsSearchResult.length === 1,
        'grid-cols-2': imgsSearchResult.length >= 2 || imgsSearchResult.length === 0,
      }"
    >
      <TheImagePreview
        v-for="img in imgsSearchResult"
        :key="img.key"
        :src="img.src"
        caption-pos="bottom-right"
        :alt="img.key"
        :class="{ 'blur-sm grayscale': isSearching }"
        transition-all duration-300
      />
    </div>
  </ThePageContent>

  <!-- Toasts, Alerts & Modals -->
  <TheToasts
    :toasts-array="toastsArray"
  />
</template>
