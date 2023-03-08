<script setup lang="ts">
defineProps<{
  captionShow?: boolean
  captionPos?: string // top-right (default) | top-left | bottom-right | bottom-left
  captionText?: string
}>()

defineOptions({
  inheritAttrs: false,
})
</script>

<template>
  <div w-sm my-6>
    <figure relative>
      <!-- img -->
      <img
        w-100
        rounded-lg object-contain
        transition-all duration-300
        shadow-xl shadow-gray-5 dark:shadow-gray-8 dark:shadow-opacity-60
        v-bind="$attrs"
      >

      <!-- img caption -->
      <figcaption
        v-if="captionText"
        absolute
        :class="{
          // default: top-right, unless specified bottom or left
          'top-4': !captionPos || !captionPos.includes('bottom'),
          'right-4': !captionPos || !captionPos.includes('left'),
          'bottom-4': captionPos && captionPos.includes('bottom'),
          'left-4': captionPos && captionPos.includes('left'),
        }"
      >
        <p
          v-if="captionShow"
          px-3 py-1
          backdrop-blur-sm rounded-lg
          text-white select-none
          class="bg-truegray-6/50"
        >
          {{ captionText }}
        </p>
      </figcaption>
    </figure>
  </div>
</template>
