<script setup lang="ts">
defineProps<{
  captionTitle?: string
  captionContent?: string
  keys: string[]
}>()
</script>

<template>
  <Transition>
    <!-- Table wrapper -->
    <div
      v-if="keys"
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
          bg-white text-gray-900 dark:bg-gray-800 dark:text-white
        >
          {{ captionTitle }}
          <p
            v-if="captionContent"
            mt-1 text-sm font-normal
            text-gray-500 dark:text-gray-400
          >
            {{ captionContent }}
          </p>
        </caption>
        <!-- Table Header -->
        <thead
          text-xs uppercase
          bg-gray-100 text-gray-700 dark:bg-gray-700 dark:text-gray-400
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
          <!-- 1st row -->
          <tr
            v-for="(key, index) in keys"
            :key="key"
            dark:border-gray-700
            :class="{
              'bg-white dark:bg-gray-900': index % 2 === 0,
              'bg-gray-200 dark:bg-gray-800': index % 2 !== 0,
              'border-b': index !== keys.length - 1,
            }"
          >
            <th
              px-6 py-3 font-medium
              scope="row"
            >
              {{ index + 1 }}
            </th>
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
