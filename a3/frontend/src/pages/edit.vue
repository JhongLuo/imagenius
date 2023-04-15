<script setup lang="ts">
import type { Image, RawImageData } from '~/composables/utils'

defineOptions({
  name: 'EditPage',
})

const api = useAPIStore()
const { toastsArray, blinkToast } = useToasts()

const canvasImg = ref<Image | undefined>()
const imgKey = computed<string>(() => useRoute().query.key as string)

const isIniting = ref<boolean>(false)
const isSaving = ref<boolean>(false)

const initCanvasImg = async () => {
  // start init
  isIniting.value = true
  const fd = new FormData()
  fd.append('key', imgKey.value)
  const response = await api.searchImagesByKey(fd)
  utilsJS.validateResponse(response)
  // handle success
  const rawData: RawImageData = response.data.image
    canvasImg.value = {
      key: rawData.key,
      src: '',
      srcSaved: rawData.src,
    } as Image
    // finish loading and start display
    await utils.sleep(50)
    isIniting.value = false
    canvasImg.value.src = canvasImg.value.srcSaved
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

onMounted(() => {
  console.log(canvasImg.value)
})
</script>

<template>
  <!-- Page Title -->
  <h1
    my-title
  >
    Edit
  </h1>

  <!-- Page Content -->
  <ThePageContent>
    key: {{ $route.query.key }}
    <TheImagePreview
      v-if="canvasImg !== undefined"
      :src="canvasImg.src"
      :alt="canvasImg.key"
      :class="{ 'blur-sm grayscale': isSaving }"
      transition-all duration-300
    />
  </ThePageContent>
</template>
