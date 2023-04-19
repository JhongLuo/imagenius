<script setup lang="ts">
import type { EditConfigOptions, Image, RawImageData, Selectable } from '~/composables/utils'

defineOptions({
  name: 'EditPage',
})

const api = useAPIStore()
const { toastsArray, blinkToast } = useToasts()

const canvasImg = ref<Image | undefined>()
const dimensionTesterImg = ref<HTMLImageElement | undefined>()
const imgDimensions = reactive<{ width: number; height: number }>({ width: 0, height: 0 })
const imgKey = computed<string>(() => useRoute().query.key as string)
const imgKeyUserInput = ref<string>('')
const editConfigs = reactive<EditConfigOptions>({
  xPos: 0,
  yPos: 0,
  radius: 0,
  prompt: '',
})
const ifFlipMaskColor = ref<boolean>(false)
watch(editConfigs, (newVal: any) => {
  newVal.xPos = newVal.xPos < 0 ? 0 : newVal.xPos > imgDimensions.width - 1 ? imgDimensions.width - 1 : Math.floor(newVal.xPos)
  newVal.yPos = newVal.yPos < 0 ? 0 : newVal.yPos > imgDimensions.height - 1 ? imgDimensions.height - 1 : Math.floor(newVal.yPos)
  newVal.radius = newVal.radius < 0 ? 0 : newVal.radius > imgDimensions.width ? imgDimensions.width : Math.floor(newVal.radius)
})
const overlayStyle = computed(() => {
  const cappedX = Math.min(editConfigs.xPos, imgDimensions.width - 1)
  const cappedY = Math.min(editConfigs.yPos, imgDimensions.height - 1)
  const cappedR = Math.min(editConfigs.radius, imgDimensions.width)
  const left = cappedX - cappedR
  const top = cappedY - cappedR
  const width = cappedR * 2
  const height = cappedR * 2
  return {
    left: `${left}px`,
    top: `${top}px`,
    width: `${width}px`,
    height: `${height}px`,
    clipPath: `polygon(${-left}px ${-top}px, ${-left + imgDimensions.width}px ${-top}px, ${-left + imgDimensions.width}px ${-top + imgDimensions.height}px, ${-left}px ${-top + imgDimensions.height}px)`,
  }
})
const isFormValid = computed<boolean>(() => editConfigs.radius > 0 && editConfigs.prompt.length > 0)

const isIniting = ref<boolean>(false)

// delete modal
const isShowingDeleteModal = ref<boolean>(false)
const isDeleting = ref<boolean>(false)
const isDeleted = ref<boolean>(false)

// new images
const numImgsResult = ref<number>(0)
const imgsGenerated = ref<(Image & Selectable)[]>([])
const imgsSelected = computed<(Image & Selectable)[]>(() => imgsGenerated.value.filter(img => img.selected))
const isGenerating = ref<boolean>(false)
const isSaving = ref<boolean>(false)
const isSelectionValid = computed<boolean>(() => imgsSelected.value.length > 0)

const initCanvasImg = async () => {
  // start init
  isIniting.value = true
  try {
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
    const testerImg = dimensionTesterImg.value!
    testerImg.onload = () => {
      imgDimensions.width = testerImg.naturalWidth
      imgDimensions.height = testerImg.naturalHeight
    }
  }
  catch (err) {
    // handle error
    blinkToast(
      TOAST_ID__INIT_IMG__ERROR,
      'error',
      err as string)
    isIniting.value = false
  }
}

const handleSubmitEdit = async () => {
  // start init
  isGenerating.value = true
  try {
    const fd = new FormData()
    fd.append('parent_key', imgKey.value)
    fd.append('prompt', editConfigs.prompt.trim())
    fd.append('x_pos', editConfigs.xPos.toString())
    fd.append('y_pos', editConfigs.yPos.toString())
    fd.append('radius', editConfigs.radius.toString())
    const response = await api.editImage(fd)
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
    blinkToast(
      TOAST_ID__EDIT_IMG__SUCCESS,
      'success',
      TOAST_MSG__EDIT_IMG__SUCCESS)
  }
  catch (err) {
    // handle error
    blinkToast(
      TOAST_ID__EDIT_IMG__ERROR,
      'error',
      err as string)
    isGenerating.value = false
  }
}

const handleDeleteImage = async () => {
  // start delete
  isDeleting.value = true
  try {
    const fd = new FormData()
    fd.append('key', imgKey.value)
    const response = await api.deleteImage(fd)
    utilsJS.validateResponse(response)
    // handle success
    await utils.sleep(50)
    isDeleted.value = true
    isDeleting.value = false
    blinkToast(
      TOAST_ID__DELETE_IMG__SUCCESS,
      'success',
      TOAST_MSG__DELETE_IMG__SUCCESS)
    await utils.sleep(1000)
    utils.navigateToListAll()
  }
  catch (err) {
    // handle error
    blinkToast(
      TOAST_ID__DELETE_IMG__ERROR,
      'error',
      err as string)
    isDeleting.value = false
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
    editConfigs.xPos = imgDimensions.width / 2
    editConfigs.yPos = imgDimensions.height / 2
    editConfigs.radius = 0
    editConfigs.prompt = ''
    imgsGenerated.value.forEach((img: (Image & Selectable)) => {
      img.src = ''
    })
    // clear displayed results
    await utils.sleep(50)
    imgsGenerated.value = []
    isSaving.value = false
    blinkToast(
      TOAST_ID__SAVE_IMGS__SUCCESS,
      'success',
      TOAST_MSG__SAVE_IMGS__SUCCESS)
    await utils.sleep(500)
    utils.navigateToTree(selectedKeys[0])
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

onMounted(() => {
  if (imgKey.value !== undefined)
    initCanvasImg()
})
</script>

<template>
  <!-- Page Title -->
  <h1
    my-title
  >
    Edit
  </h1>

  <div
    v-if="imgKey === undefined"
    w-md
    flex flex-row justify-between items-end
  >
    <div
      class="w-70%"
    >
      <TheLabeledInput
        input-id="input-edit-key"
        label-text="Image Key"
      >
        <TheIconedTextInput
          v-model.trim="imgKeyUserInput"
          icon="i-carbon:password"
          input-id="input-edit-key-str"
          placeholder="Key of img to search for..."
          @keydown.enter="utils.navigateToEdit(imgKeyUserInput)"
        />
      </TheLabeledInput>
    </div>

    <!-- button: retrieve -->
    <TheButton
      label="Go"
      :disabled="imgKeyUserInput.length === 0"
      @click="utils.navigateToEdit(imgKeyUserInput)"
    />
  </div>

  <!-- Page Content -->
  <div
    v-if="imgKey !== undefined"
    w-full
    flex flex-col items-center
  >
    <div
      v-if="canvasImg !== undefined && !isDeleted"
      class="relative"
    >
      <!-- Canvas -->
      <TheImagePreview
        :src="canvasImg.src"
        :alt="canvasImg.key"
        :class="{ 'blur-sm grayscale': isGenerating }"
        transition-all duration-300
        @click="ifFlipMaskColor = !ifFlipMaskColor"
      />

      <img
        v-if="canvasImg !== undefined"
        ref="dimensionTesterImg"
        :src="canvasImg.src"
        display-none
      >

      <!-- Mask -->
      <div
        class="absolute opacity-50 rounded-full pointer-events-none"
        :class="!ifFlipMaskColor ? 'bg-teal-300' : 'bg-red-500'"
        :style="overlayStyle"
      />
    </div>

    <div
      v-if="canvasImg !== undefined"
      my-4
      text-xs font-mono
    >
      Image is &lt;{{ imgDimensions.width }} x {{ imgDimensions.height }}>
    </div>

    <!-- Panel -->
    <!-- Input Group -->
    <TheInputGroup
      w-md
      px-8 py-6
      my-bg-secondary
      my-card my-shadow-light
    >
      <!-- Panel Title -->
      <div
        text-2xl mb-2
      >
        Edit Panel
      </div>

      <!-- Patch Radius -->
      <TheLabeledInput
        input-id="input-radius"
        label-text="Patch Radius"
      >
        <!-- row -->
        <div
          flex justify-between w-full
        >
          <!-- col: radius -->
          <div
            class="w-45%"
            flex flex-col items-center
          >
            <!-- <div
              flex w-full
            >
              <input
                id="input-patch-radius"
                v-model="editConfigs.radius"
                type="number"
                w-full h-full
                my-border rounded-r-none
                my-input text-center
                placeholder="<empty>"
              >
              <span
                inline-flex items-center px-3
                my-border rounded-l-none border-l-0
                my-input select-none
              >
                px
              </span>
            </div> -->
            <input
              id="minmax-range"
              v-model="editConfigs.radius"
              type="range"
              min="0"
              :max="imgDimensions.width / 2"
              w-full h-2 rounded-lg appearance-none cursor-pointer
              bg-gray-200 dark:bg-gray-700 my-outline-none
              my-4
            >

            <TheInputHelperText
              font-mono
              :helper-text="`Radius: ${editConfigs.radius}px`"
            />
          </div>
        </div>
      </TheLabeledInput>

      <!-- Patch Pos -->
      <TheLabeledInput
        input-id="input-pos"
        label-text="Patch Position"
      >
        <!-- row -->
        <div
          flex justify-between w-full
        >
          <!-- col: xPos -->
          <div
            class="w-45%"
            flex flex-col items-center
          >
            <!-- <div
              flex w-full
            >
              <input
                id="input-patch-x-pos"
                v-model="editConfigs.xPos"
                type="number"
                w-full h-full
                my-border rounded-r-none
                my-input text-center
                placeholder="<empty>"
              >
              <span
                inline-flex items-center px-3
                my-border rounded-l-none border-l-0
                my-input select-none
              >
                px
              </span>
            </div> -->
            <input
              id="minmax-range"
              v-model="editConfigs.xPos"
              type="range"
              min="0"
              :max="imgDimensions.width - 1"
              w-full h-2 rounded-lg appearance-none cursor-pointer
              bg-gray-200 dark:bg-gray-700 my-outline-none
              my-4
            >

            <TheInputHelperText
              font-mono
              :helper-text="`X Coord: ${editConfigs.xPos}px`"
            />
          </div>

          <!-- col: yPos -->
          <div
            class="w-45%"
            flex flex-col items-center
          >
            <!-- <div
              flex w-full
            >
              <input
                id="input-patch-y-pos"
                v-model="editConfigs.yPos"
                type="number"
                w-full h-full
                my-border rounded-r-none
                my-input text-center
                placeholder="<empty>"
              >
              <span
                inline-flex items-center px-3
                my-border rounded-l-none border-l-0
                my-input select-none
              >
                px
              </span>
            </div> -->
            <input
              id="minmax-range"
              v-model="editConfigs.yPos"
              type="range"
              min="0"
              :max="imgDimensions.height - 1"
              w-full h-2 rounded-lg appearance-none cursor-pointer
              bg-gray-200 dark:bg-gray-700 my-outline-none
              my-4
            >

            <TheInputHelperText
              font-mono
              :helper-text="`Y Coord: ${editConfigs.yPos}px`"
            />
          </div>
        </div>
      </TheLabeledInput>

      <!-- Patch Prompt -->
      <TheLabeledInput
        input-id="input-prompt"
        label-text="Patch Prompt"
      >
        <!-- row -->
        <div
          flex justify-between w-full
        >
          <div
            w-full
            flex flex-col items-center
          >
            <div
              flex w-full
            >
              <input
                id="input-patch-prompt"
                v-model="editConfigs.prompt"
                type="text"
                w-full h-full
                my-border
                my-input
                placeholder="Patch content goes here..."
              >
            </div>
          </div>
        </div>
      </TheLabeledInput>

      <!-- Button: Submit Edit -->
      <!-- Group <submit button + spinner> -->
      <div
        flex items-center space-x-3
      >
        <!-- submit button -->
        <TheButton
          text-sm
          label="Generate with Edit"
          :disabled="!isFormValid || isGenerating || isShowingDeleteModal || isDeleting || isDeleted || isSaving"
          @click="handleSubmitEdit"
        />

        <!-- delete button -->
        <button
          text-sm my-btn-danger
          :disabled="isGenerating || isShowingDeleteModal || isDeleting || isDeleted || isSaving"
          @click="isShowingDeleteModal = true || isDeleting || isSaving"
        >
          Delete Image
        </button>

        <!-- Delete Modal Content -->
        <TheModal
          v-model:is-shown="isShowingDeleteModal"
          modal-type="delete"
          :modal-id="MODAL_ID__DELETE_IMG"
          :modal-title="MODAL_TITLE__DELETE_IMG"
          :modal-description="MODAL_DESCRIPTION__DELETE_IMG"
          :action="handleDeleteImage"
        />

        <!-- spinner -->
        <TheSpinner
          v-if="isGenerating || isDeleting || isDeleted"
          alt-text="Generating..."
        />
      </div>
    </TheInputGroup>
  </div>

  <!-- New Images -->
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
    flex items-center justify-center space-x-3
  >
    <!-- spinner -->
    <TheSpinner
      v-if="isSaving"
      alt-text="Saving..."
    />

    <!-- button: save -->
    <TheButton
      label="Save"
      :disabled="!isSelectionValid || isSaving || isGenerating || isShowingDeleteModal || isDeleting || isDeleted"
      @click="handleSave"
    />
  </div>

  <!-- Toasts, Alerts & Modals -->
  <TheToasts
    :toasts-array="toastsArray"
  />
</template>

<style scoped>
#input-patch-x-pos::-webkit-outer-spin-button,
#input-patch-y-pos::-webkit-outer-spin-button,
#input-patch-radius::-webkit-outer-spin-button,
#input-patch-x-pos::-webkit-inner-spin-button,
#input-patch-y-pos::-webkit-inner-spin-button,
#input-patch-radius::-webkit-inner-spin-button
{
  -webkit-appearance: none;
  margin: 0;
}

#input-patch-x-pos,
#input-patch-y-pos,
#input-patch-radius
{
  appearance: textfield;
  -moz-appearance: textfield;
}
</style>
