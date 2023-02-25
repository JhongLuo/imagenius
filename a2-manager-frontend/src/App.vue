<template>
  <main flex flex-col justify-between p="x-4 y-10" font-sans text="center gray-700 dark:gray-200">
    <div>
      <!-- header -->
      <TheHeader />
      <!-- spacer -->
      <div py-4 />
      <!-- router content -->
      <RouterView />
    </div>
    <!-- footer -->
    <footer flex-col>
      <TheFooter />
    </footer>
  </main>
</template>

<style>
main {
  min-height: 100vh;
}
</style>
