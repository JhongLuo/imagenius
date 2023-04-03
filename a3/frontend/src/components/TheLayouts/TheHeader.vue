<template>
  <div
    flex flex-col items-center
  >
    <div flex flex-row justify-center>
      <!-- icon -->
      <div i-carbon:scan-alt text-4xl inline-block />

      <!-- spacer -->
      <div px-2 />

      <!-- title -->
      <div
        flex flex-col
        select-none
      >
        <p text-lg>
          AI Image Library
        </p>
        <p text-sm op75>
          <em>
            smart image management
          </em>
        </p>
      </div>
    </div>

    <TheNavs mt-2 />
  </div>
</template>
