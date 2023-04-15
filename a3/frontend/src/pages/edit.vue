<script setup lang="ts">
import type { EditConfigOptions, Image, RawImageData } from '~/composables/utils'

defineOptions({
  name: 'EditPage',
})

const api = useAPIStore()
const { toastsArray, blinkToast } = useToasts()

const canvasImg = ref<Image | undefined>()
const imgKey = computed<string>(() => useRoute().query.key as string)
const editConfigs = reactive<EditConfigOptions>({
  xPos: 0,
  yPos: 0,
  radius: 0,
  prompt: '',
})
const isFormValid = computed<boolean>(() => editConfigs.radius > 0 && editConfigs.prompt.length > 0)

const isIniting = ref<boolean>(false)
const isSubmittingEdit = ref<boolean>(false)

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
    blinkToast(
      TOAST_ID__INIT_IMG__SUCCESS,
      'success',
      TOAST_MSG__INIT_IMG__SUCCESS)
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
  isSubmittingEdit.value = true
  try {
    const fd = new FormData()
    fd.append('parent_key', imgKey.value)
    fd.append('x_pos', editConfigs.xPos.toString())
    fd.append('y_pos', editConfigs.yPos.toString())
    fd.append('radius', editConfigs.radius.toString())
    const response = await api.editImage(fd)
    utilsJS.validateResponse(response)
    // handle success
    const newImg: RawImageData = response.data.image
    const newKey = newImg.key
    utils.navigateToEdit(newKey)
    // finish loading and start display
    await utils.sleep(300)
    isSubmittingEdit.value = false
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
    isSubmittingEdit.value = false
  }
}

onMounted(() => {
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

  <!-- Page Content -->
  <ThePageContent>
    <TheImagePreview
      v-if="canvasImg !== undefined"
      :src="canvasImg.src"
      :alt="canvasImg.key"
      :class="{ 'blur-sm grayscale': isSubmittingEdit }"
      transition-all duration-300
    />

    <div
      my-4
      text-xs font-mono
    >
      Image is &lt;256 x 256>
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
            <div
              flex w-full
            >
              <input
                id="input-patch-x-pos"
                v-model="editConfigs.xPos"
                type="number"
                oninput="this.value = this.value > 255 ? 255 : Math.floor(this.value)"
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
            </div>

            <TheInputHelperText
              helper-text="X Coordinate"
            />
          </div>

          <!-- col: yPos -->
          <div
            class="w-45%"
            flex flex-col items-center
          >
            <div
              flex w-full
            >
              <input
                id="input-patch-y-pos"
                v-model="editConfigs.yPos"
                type="number"
                oninput="this.value = this.value > 255 ? 255 : Math.floor(this.value)"
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
            </div>

            <TheInputHelperText
              helper-text="Y Coordinate"
            />
          </div>
        </div>
      </TheLabeledInput>

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
            <div
              flex w-full
            >
              <input
                id="input-patch-radius"
                v-model="editConfigs.radius"
                type="number"
                oninput="this.value = this.value > 255 ? 255 : Math.floor(this.value)"
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
            </div>

            <TheInputHelperText
              helper-text="Radius Size"
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
      <TheButton
        text-sm
        label="Submit"
        :disabled="!isFormValid"
        @click="handleSubmitEdit"
      />
    </TheInputGroup>
  </ThePageContent>

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
