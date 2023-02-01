<template>
  <!--  Page Title  -->
  <div class="container-lg mb-5">
    <h1>Welcome to the Web Application A1!</h1>
  </div>

  <!--  Page Content: button to upload  -->
  <div class="container-lg mt-5">
    <RouterLink
      to="/upload"
      class="btn btn-secondary btn-lg"
      aria-current="page"
      >Get Started →</RouterLink
    >
  </div>
</template>

<script>
export default {
  name: "HomeView.vue",
};
</script>

<style scoped></style>
