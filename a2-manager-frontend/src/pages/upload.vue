<script setup lang="ts" generic="T extends any, O extends any">
defineOptions({
  name: 'UploadPage',
})

// const name = ref('')

// const pressed = () => {
//   console.warn(name.value)
// }
</script>

<template>
  <p my-title-style>
    Upload
  </p>
  <!-- content -->
  <div w-lg flex flex-col items-center>
    <!-- Input Group: items-start -->
    <div flex flex-col items-start>
      <!-- Input: image key  -->
      <label
        for="input-image-key"
        my-label-style
      >
        Image Key
      </label>
      <div class="relative mb-6">
        <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
          <span icon-plain i-carbon:password />
        </div>
        <input
          id="input-image-key"
          type="text"
          my-text-input-style pl-10
          placeholder="Your image key"
        >
      </div>

      <!-- Input: image file -->

      <label
        for="input-image-file"
        my-label-style
      >
        Image file
      </label>
      <input
        id="input-image-file"
        type="file"
        my-input-style block w-full cursor-pointer
        aria-describedby="file_input_help"
      >
      <p
        id="file_input_help"
        my-helper-text-style
      >
        Image format only (e.g. PNG, JPG, GIF, etc.)
      </p>
    </div>
  </div>
</template>
