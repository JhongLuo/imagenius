<script setup lang="ts">
import type { Image, Labeled, RawImageData } from '~/composables/utils'

defineOptions({
  name: 'SearchByTagPage',
})

const api = useAPIStore()
const { toastsArray, blinkToast } = useToasts()

const isGettingTags = ref(false)
const isSearching = ref(false)

const imgTags = ref<string[]>([])
const imgTagsOptions = computed<Labeled[]>(() => imgTags.value.map(tag => ({ label: tag })))

const initialTagLabel = 'Please select:'
const selectedTags = ref({ label: initialTagLabel })
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
    await utils.sleep(50)
    isGettingTags.value = false
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
    Search By Tag
  </h1>

  <!-- Page Content -->
  <ThePageContent>
    <TheListbox
      v-model="selectedTags"
      w-xs z-11
      :options="imgTagsOptions"
    />

    <!-- Search Results: -->
    <div
      w-full h-full
      mt-8
      grid gap-4
      :class="{
        'grid-cols-1': imgsSearchResult.length < 2,
        'grid-cols-2': imgsSearchResult.length >= 2,
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
