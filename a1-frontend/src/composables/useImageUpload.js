import { ref, watch } from "vue";

/**
 * Utilities for vue 3 implementation of upload action
 * @returns {{imgUrl: Ref<string>,
 *            onFileSelected: function}}
 */
export function useImageUpload() {
  const imgFile = ref("");
  const imgUrl = ref("");

  const onFileSelected = (event) => {
    // ignore when no file selected
    if (event.target.files.length === 0) {
      imgFile.value = "";
      imgUrl.value = "";
    }

    imgFile.value = event.target.files[0];
  };

  watch(imgFile, (imgFile) => {
    if (!(imgFile instanceof File)) {
      return;
    }

    let fileReader = new FileReader();
    fileReader.readAsDataURL(imgFile);
    fileReader.addEventListener("load", () => {
      imgUrl.value = fileReader.result;
      // console.log("setup -> imgUrl.value", imgUrl.value); // log base64 val
    });
  });

  return {
    imgUrl,
    onFileSelected,
  };
}
