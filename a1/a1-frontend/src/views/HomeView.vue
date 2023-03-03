<script setup>
import { useAPIStore } from '@/stores/api'
const apiStore = useAPIStore()
</script>

<template>
  <!--  Page Title  -->
  <div class="container mb-5">
    <h1>Client · Web Application A2</h1>
  </div>

  <!--  Page Content: backend form  -->
  <div class="container mb-5">
    <div class="mb-3 w-75">
      <label for="basic-url" class="form-label">Backend IP</label>
      <div class="input-group input-group-lg">
        <span class="input-group-text">http://</span>
        <input
          v-model="apiStore.ipAddr.host"
          type="text"
          class="form-control w-50"
          placeholder="hostname"
        >
        <span class="input-group-text">:</span>
        <input
          v-model="apiStore.ipAddr.port"
          type="number"
          class="form-control w-25"
          placeholder="port"
          aria-label="Port"
        >
      </div>
    </div>
  </div>

  <!--  Page Content: button to upload  -->
  <div class="container-lg">
    <RouterLink
      to="/upload"
      class="btn btn-secondary btn-lg"
      aria-current="page"
    >
      Get Started →
    </RouterLink>
  </div>
</template>

<style scoped></style>
