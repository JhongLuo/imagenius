<script setup lang="ts">
import type { Image, RawImageData } from '~/composables/utils'

defineOptions({
  name: 'SearchByPromptPage',
})

const api = useAPIStore()
const { toastsArray, blinkToast } = useToasts()

const searchPrompt = ref<string>('')
const imgsSearchResult = ref<Image[]>([])

const isSearching = ref<boolean>(false)
const wasSearched = ref<boolean>(false)

const isPromptValid = computed<boolean>(() => searchPrompt.value.length > 0)

const handleSearchByPrompt = async () => {
  // input validation
  if (!isPromptValid.value)
    return

  // start generate
  wasSearched.value = true
  isSearching.value = true
  try {
    // construct request form data
    const fd = new FormData()
    fd.append('prompt', searchPrompt.value)
    const response = await api.searchImagesByPrompt(fd)
    utilsJS.validateResponse(response)
    // handle success
    const rawDatas: RawImageData[] = response.data.images
    imgsSearchResult.value = rawDatas.map((rawData: RawImageData) => ({
      key: rawData.key,
      src: '',
      srcSaved: rawData.src,
    } as Image))
    // finish loading and start displaying results
    await utils.sleep(300)
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
    <Transition>
      <div
        v-if="wasSearched"
        mt-8
      >
        <Transition>
          <div
            v-if="isSearching"
          >
            <span
              class="text-center text-gray-500"
            >
              Searching for results...
            </span>
          </div>

          <div
            v-else-if="imgsSearchResult.length === 0"
          >
            <span
              class="text-center text-gray-500"
            >
              No results found.
            </span>
          </div>

          <div
            v-else
            w-full h-full
            grid gap-4
            :class="{
              'grid-cols-1': imgsSearchResult.length === 1,
              'grid-cols-2': imgsSearchResult.length === 2,
              'grid-cols-3': imgsSearchResult.length >= 3,
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
              @click="utils.navigateToEdit(img.key)"
            />
          </div>
        </Transition>
      </div>
    </Transition>
  </ThePageContent>

  <!-- Toasts, Alerts & Modals -->
  <TheToasts
    :toasts-array="toastsArray"
  />
</template>

<style>
.v-enter-active {
  transition: opacity 0.2s ease;
  transition-delay: 0.1s
}

.v-leave-active {
  transition: opacity 0.1s ease;
}

.v-enter-from,
.v-leave-to {
  opacity: 0;
}
</style>
