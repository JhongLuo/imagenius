<script setup lang="ts">
import { Dialog, DialogDescription, DialogPanel, DialogTitle, TransitionChild, TransitionRoot } from '@headlessui/vue'

defineProps<{
  modalId: string
  modalType: ModalType
  modalTitle: string
  modalDescription: string
  action: Function
}>()

type ModalType = 'delete' | 'submit'

const { isShown } = defineModel<{
  isShown: boolean
}>()
</script>

<template>
  <TransitionRoot
    as="template"
    :show="isShown"
  >
    <Dialog
      :id="modalId"
      as="div"
      relative z-10
      @close="isShown = false"
    >
      <!-- modal backdrop -->
      <TransitionChild
        as="template"
        enter="ease-out duration-300"
        enter-from="opacity-0"
        enter-to="opacity-100"
        leave="ease-in duration-200"
        leave-from="opacity-100"
        leave-to="opacity-0"
      >
        <div
          fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity dark:bg-black dark:bg-opacity-60
        />
      </TransitionChild>

      <div fixed inset-0 z-10 overflow-y-auto>
        <div flex min-h-full items-end justify-center p-4 text-center sm:items-center sm:p-0>
          <!-- modal content -->
          <TransitionChild
            as="template"
            enter="ease-out duration-300"
            enter-from="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
            enter-to="opacity-100 translate-y-0 sm:scale-100"
            leave="ease-in duration-200"
            leave-from="opacity-100 translate-y-0 sm:scale-100"
            leave-to="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
          >
            <DialogPanel
              relative transform overflow-hidden rounded-lg text-left shadow-xl transition-all sm:my-8 sm:w-full sm:max-w-lg
            >
              <div
                px-4 pt-5 pb-4 sm:p-6 sm:pb-4
                bg-white dark:bg-gray-800 dark:bg-op-95
              >
                <div sm:flex sm:items-start>
                  <div
                    mx-auto flex h-12 w-12 flex-shrink-0 items-center justify-center rounded-full sm:mx-0 sm:h-10 sm:w-10
                    :class="{
                      'bg-red-100 dark:bg-red-700': modalType === 'delete',
                      'bg-teal-100 dark:bg-teal-700': modalType === 'submit',
                    }"
                  >
                    <!-- modal icon -->
                    <div
                      w-6 h-6
                      :class="{
                        'text-red-600 dark:text-red-100': modalType === 'delete',
                        'text-teal-600 dark:text-teal-100': modalType === 'submit',
                      }"
                    >
                      <svg aria-hidden="true" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                        <!-- icon: exclamation mark -->
                        <path
                          v-if="modalType === 'delete'"
                          fill-rule="evenodd"
                          clip-rule="evenodd"
                          d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z"
                        />

                        <!-- icon: info -->
                        <path
                          v-else-if="modalType === 'submit'"
                          fill-rule="evenodd"
                          clip-rule="evenodd"
                          d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a.75.75 0 000 1.5h.253a.25.25 0 01.244.304l-.459 2.066A1.75 1.75 0 0010.747 15H11a.75.75 0 000-1.5h-.253a.25.25 0 01-.244-.304l.459-2.066A1.75 1.75 0 009.253 9H9z"
                        />
                        <!-- no other case since type enforcement -->
                      </svg>
                    </div>
                  </div>
                  <!-- modal text -->
                  <div mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left>
                    <DialogTitle
                      as="h3"
                      text-lg font-semibold leading-6 select-none
                      text-gray-900 dark:text-gray-100
                    >
                      {{ modalTitle }}
                    </DialogTitle>
                    <div class="mt-3">
                      <DialogDescription
                        as="p"
                        text-sm whitespace-pre-line select-none
                        text-gray-500 dark:text-gray-400
                      >
                        {{ modalDescription }}
                      </DialogDescription>
                    </div>
                  </div>
                </div>
              </div>
              <!-- modal actions -->
              <div
                px-4 py-3 sm:flex sm:flex-row-reverse sm:px-6
                bg-gray-50 dark:bg-gray-800 dark:bg-op-95
              >
                <!-- confirm button -->
                <button
                  type="button"
                  inline-flex w-full justify-center rounded-md px-3 py-2 text-sm font-semibold shadow-sm sm:ml-3 sm:w-auto

                  :class="{
                    'bg-red-600 dark:bg-red-700 hover:bg-red-700 dark:hover:bg-red-800 text-white dark:text-gray-100 ring-red-300 dark:ring-red-800': modalType === 'delete',
                    'bg-teal-600 dark:bg-teal-700 hover:bg-teal-700 dark:hover:bg-teal-800 text-white dark:text-gray-100 ring-teal-300 dark:ring-teal-800': modalType === 'submit',
                  }"
                  @click="isShown = false; action()"
                >
                  {{ modalType === 'delete' ? 'Delete' : 'Submit' }}
                </button>

                <!-- cancel button -->
                <button
                  type="button"
                  mt-3 inline-flex w-full justify-center rounded-md px-3 py-2 text-sm font-semibold shadow-sm ring-1 ring-inset sm:mt-0 sm:w-auto
                  bg-white dark:bg-gray-600 hover:bg-gray-100 dark:hover:bg-gray-700 text-gray-900 dark:text-gray-100 ring-gray-300 dark:ring-gray-800
                  @click="isShown = false"
                >
                  Cancel
                </button>
              </div>
            </DialogPanel>
          </TransitionChild>
        </div>
      </div>
    </Dialog>
  </TransitionRoot>
</template>
