<script setup lang="ts">
import type { Image, Labeled, RawImageData } from '~/composables/utils'

defineOptions({
  name: 'SearchByTagPage',
})

const api = useAPIStore()
const { toastsArray, blinkToast } = useToasts()

const isGettingTags = ref<boolean>(false)
const isSearching = ref<boolean>(false)
const isTagsLoaded = ref<boolean>(false)

const imgTags = ref<string[]>([])
const imgTagsOptions = computed<Labeled[]>(() => imgTags.value.map(tag => ({ label: tag })))
const initialTagLabel = 'Please select:'
const selectedTags = ref<Labeled>({ label: initialTagLabel })
const imgsSearchResult = ref<Image[]>([])

const handleGetTags = async () => {
  isGettingTags.value = true
  try {
    // construct request form data
    const response = await api.getTags()
    utilsJS.validateResponse(response)
    // handle success
    imgTags.value = response.data.tags
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
    fd.append('selected_tags', JSON.stringify([selectedTags.value.label]))
    const response = await api.searchImagesByTags(fd)
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

watch(selectedTags, (newVal) => {
  if (newVal.label !== initialTagLabel)
    handleSearchByTags()
})

onMounted(() => {
  handleGetTags()
})
</script>

<template>
  <!-- Page Title -->
  <h1 my-title>
    Browse By Tag
  </h1>

  <!-- Page Content -->
  <ThePageContent>
    <TheListbox
      v-model="selectedTags"
      w-xs z-11
      :options="imgTagsOptions"
    />

    <!-- Search Results: -->
    <Transition>
      <div
        v-if="isTagsLoaded"
        mt-8
      >
        <Transition>
          <div
            v-if="imgTagsOptions.length === 0"
          >
            <span
              class="text-center text-gray-500"
            >
              No tags available in library.
            </span>
          </div>

          <div
            v-else-if="selectedTags.label === initialTagLabel"
          >
            <span
              class="text-center text-gray-500"
            >
              Please select a tag to search for.
            </span>
          </div>

          <div
            v-else-if="isSearching"
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
              @click="utils.navigateToTree(img.key)"
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
