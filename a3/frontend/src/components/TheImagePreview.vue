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
  <Transition
    name="slide-fade"
  >
    <div
      v-if="$attrs.src"
      w-full flex justify-center items-start
      cursor-pointer
    >
      <figure relative>
        <!-- img -->
        <img
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
          <span
            px-3 py-1
            backdrop-blur-sm rounded-lg
            text-white select-none
            class="bg-truegray-5/50"
          >
            {{ captionText }}
          </span>
        </figcaption>
      </figure>
    </div>
  </Transition>
</template>

<style>
/* .v-enter-active,
.v-leave-active {
  transition: opacity 0.3s ease;
}

.v-enter-from,
.v-leave-to {
  opacity: 0;
} */
/*
  Enter and leave animations can use different
  durations and timing functions.
*/
.slide-fade-enter-active {
  transition: all 0.3s ease-out;
}

.slide-fade-leave-active {
  transition: all 0.2s ease-in;
}

.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateY(3px);
  opacity: 0;
}
</style>
