<script setup lang="ts">
import type { Image, RawImageData } from '~/composables/utils'

defineOptions({
  name: 'ListPage',
})

const api = useAPIStore()
const { toastsArray, blinkToast } = useToasts()

const isLoading = ref<boolean>(false)
const hasLoaded = ref<boolean>(false)
const isModalShown = ref<boolean>(false)
const isDeleting = ref<boolean>(false)

const imgsLoadResult = ref<Image[]>([])

const handleGetAllImages = async () => {
  // start generate
  hasLoaded.value = true
  isLoading.value = true
  try {
    const response = await api.getAllImages()
    utilsJS.validateResponse(response)
    // handle success
    const rawDatas: RawImageData[] = response.data.images
    imgsLoadResult.value = rawDatas.map((rawData: RawImageData) => ({
      key: rawData.key,
      src: '',
      srcSaved: rawData.src,
    } as Image))
    // finish loading and start displaying results
    await utils.sleep(300)
    isLoading.value = false
    imgsLoadResult.value.forEach((img: Image) => {
      img.src = img.srcSaved
    })
    blinkToast(
      TOAST_ID__GET_ALL_IMGS__SUCCESS,
      'success',
      TOAST_MSG__GET_ALL_IMGS__SUCCESS)
  }
  catch (err) {
    // handle error
    blinkToast(
      TOAST_ID__GET_ALL_IMGS__ERROR,
      'error',
      err as string)
    isLoading.value = false
  }
}

const handleDeleteAllImages = async () => {
  // start generate
  isDeleting.value = true
  try {
    const response = await api.deleteAllImages()
    utilsJS.validateResponse(response)
    // handle success
    const rawDatas: RawImageData[] = response.data.images
    imgsLoadResult.value = rawDatas.map((rawData: RawImageData) => ({
      key: rawData.key,
      src: '',
      srcSaved: rawData.src,
    } as Image))
    // finish loading and start displaying results
    await utils.sleep(300)
    isDeleting.value = false
    imgsLoadResult.value.forEach((img: Image) => {
      img.src = img.srcSaved
    })
    blinkToast(
      TOAST_ID__DELETE_ALL_IMGS__SUCCESS,
      'success',
      TOAST_MSG__DELETE_ALL_IMGS__SUCCESS)
  }
  catch (err) {
    // handle error
    blinkToast(
      TOAST_ID__DELETE_ALL_IMGS__ERROR,
      'error',
      err as string)
    isDeleting.value = false
  }
}

onMounted(() => {
  handleGetAllImages()
})
</script>

<template>
  <!-- Page Title -->
  <h1 my-title>
    List All Images
  </h1>

  <!-- Page Content -->
  <ThePageContent>
    <!-- Search Results: -->
    <Transition>
      <div
        v-if="hasLoaded"
        mt-8
      >
        <Transition>
          <div
            v-if="isLoading"
          >
            <span
              class="text-center text-gray-500"
            >
              Loading all images...
            </span>
          </div>

          <div
            v-else-if="imgsLoadResult.length === 0"
          >
            <span
              class="text-center text-gray-500"
            >
              No results found.
            </span>
          </div>

          <div
            v-else
            flex flex-col justify-center items-center
          >
            <div
              w-full h-full
              grid gap-4
              :class="{
                'grid-cols-1': imgsLoadResult.length === 1,
                'grid-cols-2': imgsLoadResult.length === 2,
                'grid-cols-3': imgsLoadResult.length >= 3,
              }"
            >
              <TheImagePreview
                v-for="img in imgsLoadResult"
                :key="img.key"
                :src="img.src"
                caption-pos="bottom-right"
                :alt="img.key"
                :class="{ 'blur-sm grayscale': isLoading }"
                transition-all duration-300
                @click="utils.navigateToEdit(img.key)"
              />
            </div>

            <div
              mt-8
              flex items-center space-x-3
            >
              <!-- spinner -->
              <TheSpinner
                v-if="isDeleting"
                alt-text="Saving..."
              />

              <!-- button: delete all -->
              <button
                my-btn-danger mt-8 text-sm
                @click="isModalShown = true"
              >
                Delete All
              </button>

              <!-- Delete Modal Content -->
              <TheModal
                v-model:is-shown="isModalShown"
                modal-type="delete"
                :modal-id="MODAL_ID__DELETE_ALL_IMGS"
                :modal-title="MODAL_TITLE__DELETE_ALL_IMGS"
                :modal-description="MODAL_DESCRIPTION__DELETE_ALL_IMGS"
                :action="handleDeleteAllImages"
              />
            </div>
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
