<template>
  <!--  Page Title  -->
  <div class="container mb-5">
    <h1>Upload</h1>
  </div>

  <!--  Page Content: upload form  -->
  <div class="container mb-5">
    <!--  form  -->
    <form class="px-3 py-4 mb-3 border rounded" @submit.prevent>
      <!--  image key  -->
      <div class="input-group mb-3">
        <span class="input-group-text">Image key</span>
        <input
          id="img-key"
          v-model="imgKey"
          type="text"
          class="form-control"
          placeholder="Type in your key here..."
        />
      </div>

      <!--  image file  -->
      <div class="input-group mb-3">
        <input
          id="img-file"
          type="file"
          accept="image/*"
          class="form-control"
          @change="onFileSelected"
        />
      </div>

      <!--  upload button  -->
      <button
        id="upload-button"
        class="btn btn-primary"
        type="submit"
        @click="handleUpload"
      >
        Upload
      </button>
    </form>

    <!--  image preview  -->
    <div v-show="imgUrl" class="vstack px-3 mb-5">
      <h4><span class="badge mb-2 bg-secondary">Preview:</span></h4>
      <div class="mb-3">
        <img
          id="img-display"
          class="img-thumbnail bg-light"
          :src="imgUrl"
          alt="image upload preview"
        />
      </div>
    </div>

    <!--  toasts  -->
    <div class="toast-container position-fixed bottom-0 end-0 p-3">
      <!--  error toast  -->
      <div
        id="errorToast"
        class="toast text-bg-danger"
        role="alert"
        aria-live="assertive"
        aria-atomic="true"
      >
        <div class="toast-header">
          <strong class="me-auto">ERROR</strong>
          <small>just now</small>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="toast"
            aria-label="Close"
          ></button>
        </div>
        <div class="toast-body">{{ stateErrorMsg }}</div>
      </div>

      <!--  success toast  -->
      <div
        id="successToast"
        class="toast text-bg-success"
        role="alert"
        aria-live="assertive"
        aria-atomic="true"
      >
        <div class="toast-header">
          <strong class="me-auto">SUCCESS</strong>
          <small>just now</small>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="toast"
            aria-label="Close"
          ></button>
        </div>
        <div class="toast-body">{{ stateSuccessMsg }}</div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from "vue";
import { useImageUpload } from "@/composables/useImageUpload";
import utils from "@/composables/utils";
import * as Constants from "@/composables/constants";
import { useAPIStore } from "@/stores/api";

export default {
  setup() {
    const storeAPI = useAPIStore();

    const imgKey = ref("");
    let { imgUrl, onFileSelected } = useImageUpload();
    const stateErrorMsg = ref("");
    const stateSuccessMsg = ref("");

    const handleUpload = async () => {
      // validate key
      if (!imgKey.value) {
        stateErrorMsg.value = Constants.ERR_MSG_FORM_KEY_EMPTY;
        utils.triggerToast(Constants.ID_TOAST_ERROR);
        return;
      }

      // validate file
      if (!imgUrl.value) {
        stateErrorMsg.value = Constants.ERR_MSG_FORM_FILE_EMPTY;
        utils.triggerToast(Constants.ID_TOAST_ERROR);
        return;
      }

      // fetch data
      try {
        // construct request form data
        let fd = new FormData();
        fd.append("key", imgKey.value);
        fd.append("file", imgUrl.value);
        // console.log("base64 string -> :", imgUrl.value);
        let response;
        response = await storeAPI.postImage(fd);
        // console.log(response.data);
        utils.helperThrowIfNotSuccess(response);
        // handle success
        stateSuccessMsg.value = Constants.SUCCESS_MSG_UPLOAD_IMG;
        utils.triggerToast(Constants.ID_TOAST_SUCCESS);
        imgKey.value = "";
        imgUrl.value = "";
      } catch (errMsg) {
        // handle error
        stateErrorMsg.value = errMsg;
        utils.triggerToast(Constants.ID_TOAST_ERROR);
      }
    };

    return {
      imgKey,
      imgUrl,
      onFileSelected,
      stateErrorMsg,
      stateSuccessMsg,
      handleUpload,
    };
  },
};
</script>

<style scoped>
#img-display {
  max-height: 60vh;
}
</style>
