<template>
  <!--  Page Title  -->
  <div class="container mb-5">
    <h1>Keys</h1>
  </div>

  <!--  Page Content: keys table  -->
  <div class="container-lg mt-5">
    <table class="table">
      <!-- table head -->
      <thead>
      <tr>
        <th scope="col">#</th>
        <th scope="col">Key ID</th>
      </tr>
      </thead>

      <!-- table body -->
      <tbody>
      <!-- table row -->
      <tr v-for="(key, index) in keys" :key="key.self">
        <th scope="row">{{ index + 1 }}</th>
        <td>{{ key }}</td>
      </tr>
      </tbody>
    </table>
  </div>

  <div class="my-4">
    <button class="btn btn-danger" data-bs-toggle="modal" data-bs-target="#modalDeleteConfirm">
      Delete All
    </button>
  </div>

  <!-- Delete Confirmation Modal -->
  <div class="modal fade" id="modalDeleteConfirm" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1"
       aria-labelledby="modalDeleteConfirmLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h1 class="modal-title fs-5" id="modalDeleteConfirmLabel">
            Confirm Deletion
          </h1>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <p>Are you sure you want to delete all saved keys and image data? You cannot undo this action.</p>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-outline-secondary" data-bs-dismiss="modal">Go Back</button>
          <button @click="deleteAll" type="button" class="btn btn-outline-danger">Yes, Proceed to Delete</button>
        </div>
      </div>
    </div>
  </div>

</template>

<script>
import { ref, onMounted } from "vue";
import APIEndpoints from "@/services/APIEndpoints";

export default {
  setup() {

    onMounted(() => {
      getKeys();
    });

    const keys = ref([]);

    const getKeys = async () => {
      try {
        const response = await APIEndpoints.getAllKeys();
        keys.value = response.data.keys;
      } catch (err) {
        console.error(err);
      }
    };

    const deleteAll = async () => {
      try {
        const response = await APIEndpoints.deleteAllKeysAndValues();
        if (response.data.success !== "true") throw "failure";
      } catch (err) {
        console.error(err);
      }
    };

    return {
      keys,
      getKeys,
      deleteAll
    };
  }
};
</script>

<style scoped></style>
