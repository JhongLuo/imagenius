<template>
  <!--  Page Title  -->
  <div class="container mb-5">
    <h1>Cache Config</h1>
  </div>

  <!--  Page Content  -->
  <div class="page-content container mt-5">
    <!--  Key Table Panel  -->
    <div class="mw50 container-sm mb-5 me-auto">
      <h3>Keys in Memory-Cache</h3>
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
          class="btn btn-danger"
          data-bs-toggle="modal"
          data-bs-target="#modalClearCacheConfirm"
        >
          Clear Cache
        </button>
      </div>
    </div>

    <!--  Config Panel  -->
    <div class="mw50 container-sm ms-auto">
      <h3>Mem-Cache Config</h3>

      <!--  replacement policy  -->
      <div class="my-4">
        <h5>Replacement Policy</h5>
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
        <h5>Maximum Cache Size</h5>
        <div class="input-group">
          <input
            v-model="cacheConfigs.maxSizeFactored"
            type="number"
            class="form-control"
            placeholder="Maximum Cache Size"
            aria-label="Recipient's username with two button addons"
          />
          <select
            id="maxSizeUnit"
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
  <!-- Clear Cache Confirmation Modal -->
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
            class="btn btn-outline-secondary"
            data-bs-dismiss="modal"
          >
            Go Back
          </button>
          <button
            type="button"
            class="btn btn-outline-danger"
            data-bs-dismiss="modal"
            @click="clearCache"
          >
            Clear
          </button>
        </div>
      </div>
    </div>
  </div>

  <!--  Set Replacement Policy Modal  -->
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
              cacheConfigs.sizeFactor == 1000
                ? cacheConfigs.maxSizeFactored + " KB"
                : cacheConfigs.maxSizeFactored + " MB"
            }}
          </p>
        </div>
        <div class="modal-footer">
          <button
            type="button"
            class="btn btn-outline-secondary"
            data-bs-dismiss="modal"
          >
            Go Back
          </button>
          <button
            type="button"
            class="btn btn-outline-primary"
            data-bs-dismiss="modal"
            @click="putCacheConfigs"
          >
            Confirm
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { onMounted, ref, reactive } from "vue";
import APIEndpoints from "@/services/APIEndpoints";
import utils from "@/utils/utils";

export default {
  setup: function () {
    onMounted(() => {
      getCacheKeys();
      getCacheConfigs();
    });

    const cacheKeys = ref([]);
    const cacheConfigs = reactive({
      replacementPolicy: "",
      maxSizeFactored: 0,
      sizeFactor: 1024,
    });

    const getCacheKeys = async () => {
      try {
        let response;
        response = await APIEndpoints.getCacheKeys();
        utils.helperThrowIfNotSuccess(response);
        cacheKeys.value = response.data.keys;
      } catch (err) {
        console.error(err);
      }
    };

    const getCacheConfigs = async () => {
      try {
        let response;
        response = await APIEndpoints.getCacheConfigs();
        utils.helperThrowIfNotSuccess(response);
        cacheConfigs.replacementPolicy = response.data.replacement_policy;
        cacheConfigs.maxSizeFactored =
          response.data.max_size / cacheConfigs.sizeFactor;
      } catch (err) {
        console.error(err);
      }
    };

    const putCacheConfigs = async () => {
      try {
        let data = {
          replacement_policy: cacheConfigs.replacementPolicy,
          max_size: cacheConfigs.maxSizeFactored * cacheConfigs.sizeFactor,
        };
        let response;
        response = await APIEndpoints.putCacheConfigs(data);
        utils.helperThrowIfNotSuccess(response);
        cacheConfigs.replacementPolicy = response.data.replacement_policy;
        cacheConfigs.maxSizeFactored =
          response.data.max_size / cacheConfigs.sizeFactor;
      } catch (err) {
        console.error(err);
      }
    };

    const clearCache = async () => {
      try {
        let response;
        response = await APIEndpoints.postClearCache();
        utils.helperThrowIfNotSuccess(response);
        // TODO: handle data with new format
        await getCacheKeys();
      } catch (err) {
        console.error(err);
      }
    };

    return {
      cacheKeys,
      cacheConfigs,
      getCacheKeys,
      getCacheConfigs,
      putCacheConfigs,
      clearCache,
    };
  },
};
</script>

<style scoped>
.page-content {
  justify-content: space-between;
}

.mw50 {
  float: left;
  /*min-width: 40%;*/
  max-width: 50%;
}

#maxSizeUnit {
  max-width: 6em;
}
</style>
