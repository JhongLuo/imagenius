<template>
  <nav flex justify-center items-center text-xl mt-6 inline-flex gap-2>
    <a
      icon-btn i-carbon:home
      href="/"
      title="Home"
    />

    <p mx-2>
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
      title="config"
    />

    <a
      icon-btn i-carbon:chart-line
      href="/stats"
      title="Stats"
    />

    <p mx-2>
      ·
    </p>

    <button icon-btn @click="toggleDark()">
      <div dark:i-carbon-moon i-carbon-sun />
    </button>

    <a
      icon-btn i-carbon-logo-github
      rel="noreferrer"
      href="https://github.com/JhongLuo/images-sharing-website"
      target="_blank"
      title="GitHub"
    />
  </nav>
</template>
