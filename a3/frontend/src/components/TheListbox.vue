<script setup lang="ts">
import {
  Listbox,
  ListboxButton,
  ListboxOption,
  ListboxOptions,
} from '@headlessui/vue'
import type { Labeled } from '~/composables/utils'

defineProps<{
  options: Labeled[]
}>()

const { modelValue } = defineModel<{
  modelValue: Labeled
}>()
</script>

<template>
  <Listbox
    v-model="modelValue"
  >
    <div class="relative mt-1">
      <ListboxButton
        class="relative w-full cursor-default rounded-lg  py-2 pl-3 pr-10 text-left shadow-lg focus:outline-none focus-visible:border-indigo-500 focus-visible:ring-2 focus-visible:ring-white focus-visible:ring-opacity-75 focus-visible:ring-offset-2 focus-visible:ring-offset-orange-300 sm:text-sm
            bg-white dark:bg-gray-900
            border border-gray-1 dark:border-gray-8"
      >
        <span class="block truncate">
          {{ modelValue.label }}
        </span>
        <span
          class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2"
        >
          <div
            w-5 h-5
            class=" text-gray-600 dark:text-gray-100 "
          >
            <svg aria-hidden="true" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
              <!-- icon: chevron-up-down -->
              <path
                fill-rule="evenodd"
                clip-rule="evenodd"
                d="M10 3a.75.75 0 01.55.24l3.25 3.5a.75.75 0 11-1.1 1.02L10 4.852 7.3 7.76a.75.75 0 01-1.1-1.02l3.25-3.5A.75.75 0 0110 3zm-3.76 9.2a.75.75 0 011.06.04l2.7 2.908 2.7-2.908a.75.75 0 111.1 1.02l-3.25 3.5a.75.75 0 01-1.1 0l-3.25-3.5a.75.75 0 01.04-1.06z"
              />
            </svg>
          </div>
        </span>
      </ListboxButton>

      <transition
        leave-active-class="transition duration-100 ease-in"
        leave-from-class="opacity-100"
        leave-to-class="opacity-0"
      >
        <ListboxOptions
          class="absolute mt-1 max-h-60 w-full overflow-auto rounded-md  py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm
              text-left bg-white dark:bg-gray-900"
        >
          <ListboxOption
            v-for="option in options"
            v-slot="{ active, selected }"
            :key="option.label"
            :value="option"
            as="template"
          >
            <li
              class="relative cursor-default select-none py-2 pl-10 pr-4" :class="[
                active ? 'bg-teal-50 text-teal-900 dark:bg-teal-900 dark:text-teal-100' : 'dark:text-gray-200 text-gray-800',
              ]"
            >
              <span
                class="block truncate" :class="[
                  selected ? 'font-medium' : 'font-normal',
                ]"
              >{{ option.label }}</span>
              <span
                v-if="selected"
                class="absolute inset-y-0 left-0 flex items-center pl-3
                    text-teal-700 dark:text-teal-100"
              >
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="w-5 h-5">
                  <path fill-rule="evenodd" d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z" clip-rule="evenodd" />
                </svg>
              </span>
            </li>
          </ListboxOption>
        </ListboxOptions>
      </transition>
    </div>
  </Listbox>
</template>
