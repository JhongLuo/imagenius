<script setup lang="ts">
defineOptions({
  name: 'SearchPage',
})

const api = useAPIStore()
const { toastsArray, blinkToast } = useToasts()

const searchPrompt = ref('')
const imgsSearchResult = ref<Image[]>([])

const isSearching = ref(false)

const isPromptValid = computed(() => searchPrompt.value)

const handleSearch = async () => {
  // input validation
  if (!isPromptValid.value)
    return

  // start generate
  isSearching.value = true
  try {
    // construct request form data
    const fd = new FormData()
    fd.append('prompt', searchPrompt.value)
    const response = await api.searchImages(fd)
    utilsJS.validateResponse(response)
    // handle success
    await utils.sleep(50)
    imgsSearchResult.value = []
    response.data.images.forEach((imgData: RawImageData) => {
      imgsSearchResult.value.push({
        key: imgData.key,
        src: imgData.src,
      } as Image)
    })
    blinkToast(
      TOAST_ID__SEARCH_IMGS__SUCCESS,
      'success',
      TOAST_MSG__SEARCH_IMGS__SUCCESS)
    isSearching.value = false
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
    Search
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
            @keydown.enter="handleSearch"
          />
        </TheLabeledInput>
      </div>

      <!-- Group <upload button + spinner> -->
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
          @click="handleSearch"
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
        v-for="img in imgsSearchResult"
        :key="img.key"
        :src="img.src"
        caption-pos="bottom-right"
        :caption-text="img.selected ? '✓' : ''"
        :alt="img.key"
        transition-all
        duration-300
        @click="img.selected = !img.selected"
      />
    </div>
  </ThePageContent>

  <!-- Toasts, Alerts & Modals -->
  <TheToasts
    :toasts-array="toastsArray"
  />
</template>
