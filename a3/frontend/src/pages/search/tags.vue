<script setup lang="ts">
import type { Image, Labeled, RawImageData, Selectable } from '~/composables/utils'

defineOptions({
  name: 'SearchByTagsPage',
})

const api = useAPIStore()
const { toastsArray, blinkToast } = useToasts()

const isGettingTags = ref(false)
const isSearching = ref(false)
const isTagsLoaded = ref(false)

const imgTagsOptions = ref<(Labeled & Selectable)[]>([])
const selectedTags = computed<string[]>(() => imgTagsOptions.value.filter(tag => tag.selected).map(tag => tag.label))
const imgsSearchResult = ref<Image[]>([])

const handleGetTags = async () => {
  isGettingTags.value = true
  try {
    // construct request form data
    const response = await api.getTags()
    utilsJS.validateResponse(response)
    // handle success
    const tags: string[] = response.data.tags
    imgTagsOptions.value = tags.map((tag: string) => ({ label: tag, selected: false }))
    // finish loading and start displaying results
    await utils.sleep(500)
    isGettingTags.value = false
    isTagsLoaded.value = true
    blinkToast(
      TOAST_ID__GET_TAGS__SUCCESS,
      'success',
      TOAST_MSG__GET_TAGS__SUCCESS)
  }
  catch (err) {
    // handle error
    blinkToast(
      TOAST_ID__GET_TAGS__ERROR,
      'error',
      err as string)
    isGettingTags.value = false
  }
}

const handleSearchByTags = async () => {
  isSearching.value = true
  try {
    // construct request form data
    const fd = new FormData()
    fd.append('selected_tags', JSON.stringify(selectedTags.value))
    const response = await api.searchImagesByTags(fd)
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

watch(selectedTags, () => {
  if (selectedTags.value.length !== 0)
    handleSearchByTags()
})

onMounted(() => {
  handleGetTags()
})
</script>

<template>
  <!-- Page Title -->
  <h1 my-title>
    Search By Tags
  </h1>

  <!-- Page Content -->
  <ThePageContent>
    <Transition>
      <!-- Tags Loaded: Tags Selector -->
      <TheTags
        v-if="!isGettingTags"
        v-model="imgTagsOptions"
      />

      <!-- Tags Loading: -->
      <div
        v-else
      >
        <span
          class="text-center text-gray-500"
        >
          Loading tags...
        </span>
      </div>
    </Transition>

    <!-- Search Results: -->
    <Transition>
      <div
        v-if="isTagsLoaded && imgTagsOptions.length === 0"
        mt-8
      >
        <span
          class="text-center text-gray-500"
        >
          No tags available in library.
        </span>
      </div>

      <div
        v-else-if="isTagsLoaded && imgTagsOptions.length !== 0 && isSearching"
        mt-8
      >
        <span
          class="text-center text-gray-500"
        >
          Searching for results...
        </span>
      </div>

      <div
        v-else-if="isTagsLoaded && imgTagsOptions.length !== 0 && !isSearching && selectedTags.length === 0"
        mt-8
      >
        <span
          class="text-center text-gray-500"
        >
          Please selected tags to search for.
        </span>
      </div>

      <div
        v-else-if="isTagsLoaded && imgTagsOptions.length !== 0 && !isSearching && selectedTags.length !== 0 && imgsSearchResult.length === 0"
        mt-8
      >
        <span
          class="text-center text-gray-500"
        >
          No results found.
        </span>
      </div>

      <div
        v-else-if="isTagsLoaded && imgTagsOptions.length !== 0 && !isSearching && selectedTags.length !== 0 && imgsSearchResult.length !== 0"
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

      <div
        v-else-if="isTagsLoaded && imgsSearchResult.length === 0"
        mt-8
      >
        <span
          class="text-center text-gray-500"
        >
          No results found.
        </span>
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
