<template>
  <!--  Page Title  -->
  <div class="container mb-5">
    <h1>Upload</h1>
  </div>

  <!--  Page Content: upload form  -->
  <div class="container-lg mt-5">
    <form @submit.prevent>
      <!--  image key  -->
      <div class="mb-3">
        <label for="imgKey" class="form-label">Image Key</label>
        <input
          id="img-key"
          v-model="imgKey"
          type="text"
          class="form-control"
          placeholder="e.g., id_1, id_3, ..."
        />
      </div>

      <!--  image file  -->
      <div class="mb-3">
        <label for="imgFile" class="form-label">Image File</label>
        <input
          id="img-file"
          type="file"
          accept="image/*"
          class="form-control"
          @change="onFileSelected"
        />
      </div>

      <!--  image preview  -->
      <div class="mb-3">
        <img
          v-show="imgUrl"
          id="img-display"
          :src="imgUrl"
          class="img-thumbnail"
          alt="..."
        />
      </div>

      <!--  upload button  -->
      <div class="mb-3">
        <button
          type="submit"
          class="btn btn-primary mb-3"
          @click="handleUpload"
        >
          Upload
        </button>
      </div>
    </form>
  </div>
</template>

<script>
import { ref } from "vue";
import APIEndpoints from "@/services/APIEndpoints";
import { useImageUpload } from "@/composables/useImageUpload";
import utils from "@/composables/utils";

export default {
  setup() {
    const imgKey = ref("");
    let { imgFile, imgUrl, onFileSelected } = useImageUpload();

    const handleUpload = async () => {
      try {
        let fd = new FormData();
        fd.append("key", imgKey.value);
        fd.append("file", imgFile.value);
        console.log("fd -> :", [...fd]);
        let response;
        response = await APIEndpoints.postImage(fd);
        console.log(response);
        utils.helperThrowIfNotSuccess(response);
        // TODO: add var cleanup here
      } catch (err) {
        // TODO: add error handling here
        console.error(err);
      }
    };

    return {
      imgKey,
      imgUrl,
      onFileSelected,
      handleUpload,
    };
  },
};
</script>

<style scoped>
#img-display {
  max-height: 24em;
}
</style>
