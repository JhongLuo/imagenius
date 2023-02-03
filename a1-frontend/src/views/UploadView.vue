<template>
  <!--  Page Title  -->
  <div class="container mb-5">
    <h1>Upload</h1>
  </div>

  <!--  Page Content: upload form  -->
  <div class="container-lg mt-5">
    <div class="mb-3">
      <label for="imgKey" class="form-label">Image Key</label>
      <input
        id="imgKey"
        type="text"
        class="form-control"
        placeholder="e.g., ece1779a1_1"
      />
    </div>
    <div class="mb-3">
      <label for="imgFile" class="form-label">Image File</label>
      <input id="imgFile" type="file" class="form-control" />
    </div>
    <div class="mb-3">
      <button type="submit" class="btn btn-primary mb-3">Submit</button>
    </div>
  </div>
</template>

<script>
export default {
  name: "UploadView.vue",
};
</script>

<style scoped></style>
