<script setup lang="ts">
defineProps<{
  captionPos?: string // top-right (default) | top-left | bottom-right | bottom-left
  captionText?: string
}>()

defineOptions({
  inheritAttrs: false,
})
</script>

<template>
  <Transition>
    <div
      v-if="$attrs.src"
      w-sm my-6
    >
      <figure relative>
        <!-- img -->
        <img
          w-100
          my-card my-shadow-heavy object-contain
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
  </Transition>
</template>

<style>
.v-enter-active,
.v-leave-active {
  transition: opacity 0.3s ease;
}

.v-enter-from,
.v-leave-to {
  opacity: 0;
}
</style>
