<script setup lang="ts">
</script>

<template>
  <main
    min-h-screen px-4 py-10
    flex flex-col justify-between items-center
    font-sans
    text-center
  >
    <!-- header + content -->
    <div>
      <TheHeader />

      <!-- spacer -->
      <div py-5 />

      <RouterView />
    </div>

    <!-- footer -->
    <footer flex-col mt-16>
      <TheFooter />
    </footer>
  </main>
</template>
