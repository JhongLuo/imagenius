<template>
  <div
    flex flex-col items-center
  >
    <div flex flex-row justify-center mb-2>
      <!-- icon -->
      <div i-carbon:scan-alt text-4xl inline-block />

      <!-- spacer -->
      <div px-2 />

      <!-- title -->
      <div
        flex flex-col
        select-none
      >
        <p text-xl>
          ImaGenius
        </p>
        <p text-sm op75>
          <em>
            Smart Image Management
          </em>
        </p>
      </div>
    </div>

    <TheNavs mt-2 />
  </div>
</template>
