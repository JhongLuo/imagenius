<script setup lang="ts" generic="T extends any, O extends any">
defineOptions({
  name: 'UploadPage',
})

const imgKey = ref('')
const pressed = () => {
  // if (name)
  //   router.push(`/hi/${encodeURIComponent(name)}`)
  console.warn(typeof imgKey.value)
}
</script>

<template>
  <!-- Page Title -->
  <h1 my-title-style>
    Upload
  </h1>

  <!-- Page Content -->
  <div w-lg flex flex-col items-center>
    <!-- Input group: -->
    <div flex flex-col items-start>
      <!-- Input: image key  -->
      <label
        for="input-image-key"
        my-label-style
      >
        Image Key
      </label>
      <div class="relative mb-4">
        <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
          <span icon-plain i-carbon:password />
        </div>
        <TheTextInput
          id="input-image-key"
          v-model="imgKey"
          pl-10
          placeholder="Your image key"
        />
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
        my-input-style text-xs
        block w-full cursor-pointer rounded-lg
        aria-describedby="file_input_help"
      >
      <p
        id="file_input_help"
        my-helper-text-style
      >
        Image format only (e.g. PNG, JPG, GIF, etc.)
      </p>

      <!-- Button: upload -->
      <button
        my-btn-primary mt5
        :disabled="!imgKey"
        @click="pressed"
      >
        Upload
      </button>
    </div>
  </div>
</template>
