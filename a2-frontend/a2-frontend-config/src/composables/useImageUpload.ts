/**
 * Utilities for vue 3 implementation of upload action
 * @returns {{imgStr: Ref<string>,
 *            updateImgFile: (e: Event) => void}}
 */
export function useImageUpload() {
  const imgFile = ref<File>() // empty file
  const imgStr = ref('')

  const updateImgFile = (event: Event) => {
    const fileList = (event.target as HTMLInputElement).files ?? []
    imgFile.value = fileList[0] // will be undefined if no file selected
  }

  // watch for file changes and update imgStr
  watch(imgFile, (imgFile) => {
    // flush imgStr and skip conversion if no file selected
    if (!imgFile) {
      imgStr.value = ''
      return
    }
    // convert file to base64 string
    const fileReader = new FileReader()
    fileReader.readAsDataURL(imgFile)
    fileReader.addEventListener('load', () => {
      imgStr.value = fileReader.result as string
    })
  })

  return {
    imgStr,
    updateImgFile,
  }
}
