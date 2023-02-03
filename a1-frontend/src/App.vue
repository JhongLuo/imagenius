<script setup>
import { RouterLink, RouterView } from "vue-router";
</script>

<template>
  <nav class="navbar navbar-expand-lg bg-dark">
    <div class="container-fluid">
      <RouterLink to="/" class="ms-5 my-2 link-light navbar-brand"
        >Home
      </RouterLink>
      <div id="navbarNav" class="me-5 d-flex flex-row-reverse">
        <ul class="navbar-nav">
          <li class="mx-1 nav-item">
            <RouterLink
              to="/upload"
              class="link-secondary nav-link"
              active-class="link-light active"
              aria-current="page"
            >
              Upload
            </RouterLink>
          </li>

          <li class="mx-1 nav-item">
            <RouterLink
              to="/query"
              class="link-secondary nav-link"
              active-class="link-light active"
              aria-current="page"
            >
              Query
            </RouterLink>
          </li>

          <li class="mx-1 nav-item">
            <RouterLink
              to="/keys"
              class="link-secondary nav-link"
              active-class="link-light active"
              aria-current="page"
            >
              Keys
            </RouterLink>
          </li>

          <li class="mx-1 nav-item">
            <RouterLink
              to="/config"
              class="link-secondary nav-link"
              active-class="link-light active"
              aria-current="page"
            >
              Config
            </RouterLink>
          </li>

          <li class="mx-1 nav-item">
            <RouterLink
              to="/stats"
              class="link-secondary nav-link"
              active-class="link-light active"
              aria-current="page"
            >
              Stats
            </RouterLink>
          </li>
        </ul>
      </div>
    </div>
  </nav>

  <main class="container py-5 px-5 mx-auto">
    <RouterView />
  </main>
</template>

<style></style>
