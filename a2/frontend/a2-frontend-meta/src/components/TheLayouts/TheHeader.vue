<template>
  <div
    flex flex-col items-center
  >
    <div flex flex-row justify-center items-center>
      <!-- icon -->
      <div i-carbon:accumulation-snow text-4xl inline-block />

      <!-- spacer -->
      <div px-2 />

      <!-- title -->
      <div
        flex flex-col
        select-none
      >
        <p text-lg>
          A2 Meta Config
        </p>
        <p text-sm op75>
          <em>
            some secret sh*t you probably don't
          </em>
        </p>
        <p text-sm op75>
          <em>
            need to know about
          </em>
        </p>
      </div>
    </div>

    <TheNavs mt-2 />
  </div>
</template>
