<script setup lang="ts">
const api = useAPIStore()
</script>

<template>
  <div flex-col space-y-3 mt-6>
    <div flex justify-center items-baseline>
      <span
        my-helper-text select-none
      >
        Currently connecting to&nbsp;
      </span>
      <span
        px-1.5 py-1 rounded bg-gray-4 bg-op-15
        my-helper-text font-mono my-text-color-primary
      >
        {{ api.baseURLShort }}
      </span>
    </div>
    <nav flex justify-center items-center text-xl mt-6 space-x-3>
      <a
        icon-btn i-carbon:home
        href="/"
        title="Home"
      />

      <p mx-1 select-none>
        ·
      </p>

      <a
        icon-btn i-carbon:cloud-upload
        href="/upload"
        title="Upload"
      />

      <a
        icon-btn i-carbon:cloud-download
        href="/retrieve"
        title="Retrieve"
      />

      <a
        icon-btn i-carbon:virtual-column-key
        href="/keys"
        title="Keys"
      />

      <a
        icon-btn i-carbon:settings-adjust
        href="/config"
        title="Config"
      />

      <a
        icon-btn i-carbon:chart-line
        href="/stats"
        title="Stats"
      />

      <p mx-1 select-none>
        ·
      </p>

      <button
        icon-btn dark:i-carbon-moon i-carbon-sun
        title="Toggle Color Scheme"
        @click="toggleDark()"
      />

      <a
        icon-btn i-carbon-logo-github
        rel="noreferrer"
        href="https://github.com/JhongLuo/images-sharing-website"
        target="_blank"
        title="GitHub Repo"
      />
    </nav>
  </div>
</template>
