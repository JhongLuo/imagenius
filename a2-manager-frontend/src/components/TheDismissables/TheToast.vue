<script setup lang="ts">
defineProps<{
  toastId: string
  toastType: ToastType
  toastText: string
}>()

const { isShown } = defineModel<{
  isShown: boolean
}>()
</script>

<template>
  <Transition
    name="slide-fade"
  >
    <!-- toast element -->
    <div
      v-if="isShown"
      :id="toastId"
      role="toast"
      w-full max-w-xs rounded-lg
      p-4 mb-4
      flex items-center space-x-3
      text-gray-500 bg-gray-100 dark:text-gray-400 dark:bg-gray-800
      shadow-xl shadow-gray-5 shadow-op-30 dark:shadow-gray-7 dark:shadow-op-30
    >
      <!-- check / cross / warning icon -->
      <div
        w-8 h-8 rounded-lg
        inline-flex items-center justify-center flex-shrink-0
        :class="{
          'bg-teal-100 text-teal-400 dark:bg-teal-800 dark:text-teal-200': toastType === 'success',
          'bg-red-200 text-red-500 dark:bg-red-800 dark:text-red-200': toastType === 'error',
          'bg-yellow-200 text-yellow-500 dark:bg-yellow-800 dark:text-yellow-200': toastType === 'warning',
          'bg-blue-200 text-blue-500 dark:bg-blue-800 dark:text-blue-200': toastType === 'info',
          // no other case since type enforcement
        }"
      >
        <svg aria-hidden="true" class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
          <!-- check icon -->
          <path
            v-if="toastType === 'success'"
            fill-rule="evenodd"
            clip-rule="evenodd"
            d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
          />
          <!-- cross icon -->
          <path
            v-else-if="toastType === 'error'"
            fill-rule="evenodd"
            clip-rule="evenodd"
            d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
          />
          <!-- warning icon -->
          <path
            v-else-if="toastType === 'warning'"
            fill-rule="evenodd"
            clip-rule="evenodd"
            d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z"
          />
          <!-- info icon -->
          <path
            v-else-if="toastType === 'info'"
            fill-rule="evenodd"
            clip-rule="evenodd"
            d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a.75.75 0 000 1.5h.253a.25.25 0 01.244.304l-.459 2.066A1.75 1.75 0 0010.747 15H11a.75.75 0 000-1.5h-.253a.25.25 0 01-.244-.304l.459-2.066A1.75 1.75 0 009.253 9H9z"
          />
          <!-- no other case since type enforcement -->

        </svg>
        <span class="sr-only">
          Toast icon
        </span>
      </div>

      <!-- toast message -->
      <span
        ml-3 text-start
        text-sm font-black
        overflow-hidden text-ellipsis line-clamp-4
      >
        {{ toastText }}
      </span>

      <!-- close button -->
      <button
        :id="`${toastId}-close`"
        type="button"
        h-8 w-8 inline-flex rounded-lg
        class="ml-auto -mx-1.5 -my-1.5 p-1.5"
        focus:ring-2 focus:ring-gray-300
        bg-gray-100 hover:bg-gray-200 text-gray-400 hover:text-gray-600
        dark:bg-gray-800 dark:hover:bg-gray-700 dark:text-gray-500 dark:hover:text-white
        aria-label="Close"
        @click="isShown = false"
      >
        <svg aria-hidden="true" class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" /></svg>
        <span class="sr-only">
          Close
        </span>
      </button>
    </div>
  </Transition>
</template>

<style>
.slide-fade-enter-active {
  transition: all 0.1s ease-out;
}

.slide-fade-leave-active {
  transition: all 0.6s cubic-bezier(1, 0.5, 0.8, 1);
}

.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateX(20px);
  opacity: 0;
}
</style>
