<template>
  <div
    flex flex-col items-center
  >
    <div flex flex-row justify-center>
      <!-- icon -->
      <div i-carbon:cloud-services text-4xl inline-block />

      <!-- spacer -->
      <div px-2 />

      <!-- title -->
      <div
        flex flex-col
        select-none
      >
        <p text-lg>
          A2 Manager Web Frontend
        </p>
        <p text-sm op75>
          <em>
            Memcache Pool Management
          </em>
        </p>
      </div>
    </div>

    <TheNavs mt-2 />
  </div>
</template>
