<script setup>
import { onMounted, ref } from 'vue'
import utils from '@/composables/utils'
import * as Constants from '@/composables/constants'
import { useAPIStore } from '@/stores/api'

const storeAPI = useAPIStore()

const keys = ref([])
const stateErrorMsg = ref('')
const stateSuccessMsg = ref('')

const handleGetKeys = async (ifSkipSuccessToast = false) => {
  // fetch data
  try {
    const response = await storeAPI.getAllKeys()
    utils.helperThrowIfNotSuccess(response)
    // handle success
    // console.log(response.data);
    keys.value = response.data.keys
    if (!ifSkipSuccessToast) {
      stateSuccessMsg.value = Constants.SUCCESS_MSG_GET_KEYS
      utils.triggerToast(Constants.ID_TOAST_SUCCESS)
    }
  }
  catch (errMsg) {
    // handle error
    stateErrorMsg.value = errMsg
    utils.triggerToast(Constants.ID_TOAST_ERROR)
  }
}

const handleDeleteAll = async () => {
  // fetch data
  try {
    const response = await storeAPI.postDeleteAllData()
    utils.helperThrowIfNotSuccess(response)
    // handle success
    stateSuccessMsg.value = Constants.SUCCESS_MSG_DELETE_KEYS
    utils.triggerToast(Constants.ID_TOAST_SUCCESS)
    await handleGetKeys(true)
  }
  catch (errMsg) {
    // handle error
    stateErrorMsg.value = errMsg
    utils.triggerToast(Constants.ID_TOAST_ERROR)
  }
}
onMounted(() => {
  handleGetKeys()
})
</script>

<template>
  <!--  Page Title  -->
  <div class="container mb-5">
    <h1>Keys</h1>
  </div>

  <!--  Page Content: keys table  -->
  <div class="container-lg mb-3">
    <table class="table">
      <!-- table head -->
      <thead>
        <tr>
          <th scope="col">
            #
          </th>
          <th scope="col">
            Key Value
          </th>
        </tr>
      </thead>

      <!-- table body -->
      <tbody>
        <!-- table row -->
        <tr v-for="(key, index) in keys" :key="key.self">
          <th scope="row">
            {{ index + 1 }}
          </th>
          <td>{{ key }}</td>
        </tr>
      </tbody>
    </table>
  </div>

  <!-- Delete All Button -->
  <div class="container">
    <button
      class="btn btn-outline-danger"
      data-bs-toggle="modal"
      data-bs-target="#modalDeleteConfirm"
    >
      Delete All
    </button>
  </div>

  <!-- Delete Confirmation Modal -->
  <div
    id="modalDeleteConfirm"
    class="modal fade"
    data-bs-backdrop="static"
    data-bs-keyboard="false"
    tabindex="-1"
    aria-labelledby="modalDeleteConfirmLabel"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h1 id="modalDeleteConfirmLabel" class="modal-title fs-5">
            Confirm
          </h1>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
          />
        </div>
        <div class="modal-body">
          <p>
            Are you sure you want to delete all saved keys and image data? You
            cannot undo this action.
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
            @click="handleDeleteAll"
          >
            Delete
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
        <small>{{ storeAPI.baseURLShort }}</small>
        <button
          type="button"
          class="btn-close"
          data-bs-dismiss="toast"
          aria-label="Close"
        />
      </div>
      <div class="toast-body">
        {{ stateErrorMsg }}
      </div>
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
        <small>{{ storeAPI.baseURLShort }}</small>
        <button
          type="button"
          class="btn-close"
          data-bs-dismiss="toast"
          aria-label="Close"
        />
      </div>
      <div class="toast-body">
        {{ stateSuccessMsg }}
      </div>
    </div>
  </div>
</template>

<style scoped></style>
