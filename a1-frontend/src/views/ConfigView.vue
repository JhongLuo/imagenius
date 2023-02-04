<template>
  <!--  Page Title  -->
  <div class="container mb-5">
    <h1>Cache Config</h1>
  </div>

  <!--  Page Content  -->
  <div class="container-lg hstack align-items-start px-0 mb-3">
    <!--  Key Table Panel  -->
    <div class="container me-4">
      <!--  panel title  -->
      <h4 class="mb-3">Keys in Memory-Cache</h4>

      <!--  key table  -->
      <table class="table">
        <!-- table head -->
        <thead>
          <tr>
            <th scope="col">#</th>
            <th scope="col">Key Value</th>
          </tr>
        </thead>

        <!-- table body -->
        <tbody>
          <!-- table row -->
          <tr v-for="(key, index) in cacheKeys" :key="key.self">
            <th scope="row">{{ index + 1 }}</th>
            <td>{{ key }}</td>
          </tr>
        </tbody>
      </table>

      <!-- Clear Cache Button -->
      <div class="my-4">
        <button
          class="btn btn-outline-danger"
          data-bs-toggle="modal"
          data-bs-target="#modalClearCacheConfirm"
        >
          Clear Cache
        </button>
      </div>
    </div>

    <!--  Config Panel  -->
    <div id="config-panel" class="container ms-auto">
      <!--  panel title  -->
      <h4 class="mb-3">Mem-Cache Config</h4>

      <!--  replacement policy  -->
      <div class="my-4">
        <h6 class="mb-3">Replacement Policy</h6>
        <div class="input-group">
          <select
            id="replacementPolicy"
            v-model="cacheConfigs.replacementPolicy"
            class="form-select"
            aria-label="Memory Cache Replacement Policy"
          >
            <option disabled>Please choose one:</option>
            <option value="random">Random Replacement</option>
            <option value="LRU">Least Recently Used</option>
          </select>
        </div>
      </div>

      <!--  max cache size  -->
      <div class="my-4">
        <h6 class="mb-3">Maximum Cache Size</h6>
        <div class="input-group">
          <input
            v-model="cacheConfigs.maxSizeFactored"
            type="number"
            class="form-control"
            placeholder="Maximum Cache Size"
            aria-label="Recipient's username with two button addons"
          />
          <select
            id="unit-select"
            v-model="cacheConfigs.sizeFactor"
            class="form-select"
            aria-label="Size Unit"
          >
            <option disabled>Please choose one:</option>
            <option value="1048576">MB</option>
            <option value="1024">KB</option>
          </select>
        </div>
      </div>

      <!--  button  -->
      <div class="my-4">
        <button
          class="btn btn-primary"
          data-bs-toggle="modal"
          data-bs-target="#modalPutConfigsConfirm"
        >
          Save
        </button>
      </div>
    </div>
  </div>

  <!--  modals  -->
  <!-- Modal: Clear Cache Confirmation -->
  <div
    id="modalClearCacheConfirm"
    class="modal fade"
    data-bs-backdrop="static"
    data-bs-keyboard="false"
    tabindex="-1"
    aria-labelledby="modalClearCacheConfirmLabel"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h1 id="modalClearCacheConfirmLabel" class="modal-title fs-5">
            Confirmation
          </h1>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
          ></button>
        </div>
        <div class="modal-body">
          <p>
            Are you sure you want to clear the cache data? You will not be able
            to undo this action.
          </p>
        </div>
        <div class="modal-footer">
          <button
            type="button"
            class="btn btn-secondary"
            data-bs-dismiss="modal"
          >
            Go Back
          </button>
          <button
            type="button"
            class="btn btn-outline-danger"
            data-bs-dismiss="modal"
            @click="handleClearCache"
          >
            Clear
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- Modal: Set Replacement Policy  -->
  <div
    id="modalPutConfigsConfirm"
    class="modal fade"
    data-bs-backdrop="static"
    data-bs-keyboard="false"
    tabindex="-1"
    aria-labelledby="modalPutConfigsConfirmLabel"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h1 id="modalPutConfigsConfirmLabel" class="modal-title fs-5">
            Confirmation
          </h1>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
          ></button>
        </div>
        <div class="modal-body">
          <p>Set replacement policy: {{ cacheConfigs.replacementPolicy }}</p>
          <p>
            Set max cache size:
            {{
              cacheConfigs.sizeFactor == 1024
                ? cacheConfigs.maxSizeFactored + " KB"
                : cacheConfigs.maxSizeFactored + " MB"
            }}
          </p>
        </div>
        <div class="modal-footer">
          <button
            type="button"
            class="btn btn-secondary"
            data-bs-dismiss="modal"
          >
            Go Back
          </button>
          <button
            type="button"
            class="btn btn-primary"
            data-bs-dismiss="modal"
            @click="handlePutCacheConfigs"
          >
            Confirm
          </button>
        </div>
      </div>
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

    <!--  extra: config load success toast  -->
    <div
      id="successToastExtra"
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
      <div class="toast-body">{{ stateSuccessMsgExtra }}</div>
    </div>
  </div>
</template>

<script>
import { onMounted, ref, reactive } from "vue";
import APIEndpoints from "@/services/APIEndpoints";
import utils from "@/composables/utils";
import * as Constants from "@/composables/constants";

export default {
  setup() {
    onMounted(() => {
      handleGetCacheKeys();
      handleGetCacheConfigs();
    });

    const cacheKeys = ref([]);
    const cacheConfigs = reactive({
      replacementPolicy: "",
      maxSizeFactored: 0,
      sizeFactor: 1048576,
    });
    const stateErrorMsg = ref("");
    const stateSuccessMsg = ref("");
    const stateSuccessMsgExtra = ref("");

    const handleGetCacheKeys = async (ifSkipSuccessToast = false) => {
      // fetch data
      try {
        let response;
        response = await APIEndpoints.getCacheKeys();
        utils.helperThrowIfNotSuccess(response);
        // handle success
        cacheKeys.value = response.data.keys;
        if (!ifSkipSuccessToast) {
          stateSuccessMsg.value = Constants.SUCCESS_MSG_GET_KEYS;
          utils.triggerToast(Constants.ID_TOAST_SUCCESS);
        }
      } catch (errMsg) {
        // handle error
        stateErrorMsg.value = errMsg;
        utils.triggerToast(Constants.ID_TOAST_ERROR);
      }
    };

    const handleGetCacheConfigs = async () => {
      // fetch data
      try {
        let response;
        response = await APIEndpoints.getCacheConfigs();
        utils.helperThrowIfNotSuccess(response);
        // handle success
        cacheConfigs.replacementPolicy = response.data.replacement_policy;
        cacheConfigs.maxSizeFactored =
          response.data.max_size / cacheConfigs.sizeFactor;
        stateSuccessMsgExtra.value = Constants.SUCCESS_MSG_GET_CONFIGS;
        utils.triggerToast(Constants.ID_TOAST_SUCCESS_EXTRA);
      } catch (errMsg) {
        // handle error
        stateErrorMsg.value = errMsg;
        utils.triggerToast(Constants.ID_TOAST_ERROR);
      }
    };

    const handleClearCache = async () => {
      // fetch data
      try {
        let response;
        response = await APIEndpoints.postClearCache();
        utils.helperThrowIfNotSuccess(response);
        // handle success
        stateSuccessMsg.value = Constants.SUCCESS_MSG_DELETE_KEYS;
        utils.triggerToast(Constants.ID_TOAST_SUCCESS);
        await handleGetCacheKeys(true);
      } catch (errMsg) {
        // handle error
        stateErrorMsg.value = errMsg;
        utils.triggerToast(Constants.ID_TOAST_ERROR);
      }
    };

    const handlePutCacheConfigs = async () => {
      // fetch data
      try {
        // construct request data
        let data = {
          replacement_policy: cacheConfigs.replacementPolicy,
          max_size: cacheConfigs.maxSizeFactored * cacheConfigs.sizeFactor,
        };
        let response;
        response = await APIEndpoints.putCacheConfigs(data);
        utils.helperThrowIfNotSuccess(response);
        // handle success
        cacheConfigs.replacementPolicy = response.data.replacement_policy;
        cacheConfigs.maxSizeFactored =
          response.data.max_size / cacheConfigs.sizeFactor;
        stateSuccessMsg.value = Constants.SUCCESS_MSG_PUT_CONFIGS;
        utils.triggerToast(Constants.ID_TOAST_SUCCESS);
      } catch (errMsg) {
        // handle error
        stateErrorMsg.value = errMsg;
        utils.triggerToast(Constants.ID_TOAST_ERROR);
      }
    };

    return {
      cacheKeys,
      cacheConfigs,
      stateErrorMsg,
      stateSuccessMsg,
      stateSuccessMsgExtra,
      handlePutCacheConfigs,
      handleClearCache,
    };
  },
};
</script>

<style scoped>
#config-panel {
  max-width: 35%;
}

#unit-select {
  max-width: 5em;
}
</style>
