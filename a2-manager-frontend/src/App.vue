<template>
  <main h-screen flex flex-col justify-between items-center p="x-4 y-10" font-sans text="center gray-700 dark:gray-200">
    <!-- header + content -->
    <div>
      <TheHeader />

      <!-- spacer -->
      <div py-5 />

      <RouterView />
    </div>

    <!-- footer -->
    <footer flex-col>
      <TheFooter />
    </footer>
  </main>
</template>
