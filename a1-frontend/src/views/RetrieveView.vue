<template>
  <!--  Page Title  -->
  <div class="container mb-5">
    <h1>Retrieve</h1>
  </div>

  <!--  Page Content: result component -->
  <div class="container-lg mb-5">
    <!--  form  -->
    <form class="input-group mb-3" @submit.prevent>
      <!--  img key  -->
      <div class="form-floating">
        <input
          id="img-key"
          v-model="imgKey"
          type="text"
          class="form-control"
          placeholder="Type in your key here..."
        />
        <label for="img-key">Image key</label>
      </div>

      <!--  submit button  -->
      <button
        id="submit-button"
        class="btn btn-primary"
        type="submit"
        @click="handleRetrieve"
      >
        Submit
      </button>
    </form>

    <!--  image result  -->
    <div v-show="imgUrl" class="vstack mb-5">
      <h4><span class="badge mb-2 bg-secondary">Result:</span></h4>
      <div class="mb-3">
        <img
          id="img-display"
          class="img-thumbnail bg-light"
          :src="imgUrl"
          alt="image retrieval result"
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
import utils from "@/composables/utils";
import * as Constants from "@/composables/constants";
import { useAPIStore } from "@/stores/api";

export default {
  setup() {
    const storeAPI = useAPIStore();

    const imgKey = ref("");
    const imgUrl = ref("");
    const stateErrorMsg = ref("");
    const stateSuccessMsg = ref("");

    const handleRetrieve = async () => {
      // validate key
      if (!imgKey.value) {
        stateErrorMsg.value = Constants.ERR_MSG_FORM_KEY_EMPTY;
        utils.triggerToast(Constants.ID_TOAST_ERROR);
        return;
      }

      // fetch data
      try {
        let response;
        response = await storeAPI.getImage(imgKey.value);
        utils.helperThrowIfNotSuccess(response);
        // handle success
        imgUrl.value = response.data.content;
        stateSuccessMsg.value = Constants.SUCCESS_MSG_RETRIEVE_IMG;
        utils.triggerToast(Constants.ID_TOAST_SUCCESS);
      } catch (errMsg) {
        // handle error
        stateErrorMsg.value = errMsg;
        utils.triggerToast(Constants.ID_TOAST_ERROR);
      }
    };

    return {
      imgKey,
      imgUrl,
      stateErrorMsg,
      stateSuccessMsg,
      handleRetrieve,
    };
  },
};
</script>

<style scoped>
#img-display {
  max-height: 60vh;
}
</style>
