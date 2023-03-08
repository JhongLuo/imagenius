<script setup lang="ts">
defineProps<{
  data: string[]
  tableTitle?: string
  tableDescription?: string
  deleteText: string
  deleteAction: Function
}>()

const isShown = ref(false)
</script>

<template>
  <Transition>
    <!-- Table wrapper -->
    <div
      overflow-x-auto
      shadow-md rounded-lg
    >
      <!-- Table -->
      <table
        w-full rounded-lg
        text-sm text-center
        text-gray-500 dark:text-gray-400
      >
        <caption
          p-5 text-lg font-semibold text-left
          bg-white text-gray-900 dark:bg-gray-800 dark:text-white select-none
        >
          {{ tableTitle }}
          <p
            v-if="tableDescription"
            mt-1 text-sm font-normal
            text-gray-500 dark:text-gray-400 select-none
          >
            {{ tableDescription }}
          </p>

          <!-- Delete Modal toggle -->
          <button
            v-if="data.length > 0"
            my-btn-danger text-sm px-2 mt-2
            @click="isShown = true"
          >
            Delete All
          </button>

          <!-- Delete Modal Content -->
          <TheModal
            v-model:is-shown="isShown"
            :modal-id="MODAL_ID_DELETE_ALL_KEYS"
            modal-type="delete"
            :modal-title="MODAL_TITLE_DELETE_ALL_KEYS"
            :modal-description="MODAL_DESCRIPTION_DELETE_ALL_KEYS"
            :action="deleteAction"
          />
        </caption>
        <!-- Table Header -->
        <thead
          text-xs uppercase
          bg-gray-100 text-gray-700 dark:bg-gray-700 dark:text-gray-400 select-none
        >
          <tr>
            <th scope="col" px-12 py-2>
              Key Index
            </th>
            <th scope="col" px-12 py-2>
              Key Value
            </th>
          </tr>
        </thead>

        <!-- Table Body -->
        <tbody>
          <!-- if keys empty -->
          <tr
            v-if="data.length === 0"
            class="bg-white dark:bg-gray-900"
          >
            <td
              colspan="2"
              px-6 py-3 font-medium
              scope="row"
            >
              {{ MSG_ERROR_EMPTY_ALL_KEYS }}
            </td>
          </tr>

          <!-- if keys not empty: row for each key -->
          <tr
            v-for="(key, index) in data"
            :key="key"
            dark:border-gray-700
            :class="{
              'bg-white dark:bg-gray-900': index % 2 === 0,
              'bg-gray-200 dark:bg-gray-800': index % 2 !== 0,
              'border-b': index !== data.length - 1,
            }"
          >
            <td
              px-6 py-3 font-medium
              scope="row"
            >
              {{ index + 1 }}
            </td>
            <td
              px-6 py-3
              text-gray-900 dark:text-white
            >
              {{ key }}
            </td>
          </tr>
        </tbody>
      </table>
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
