<template>
  <nav flex justify-center items-center text-xl space-x-3>
    <a
      icon-btn i-carbon:home
      href="/"
      title="Home"
    />

    <p mx-1 select-none>
      ·
    </p>

    <a
      icon-btn i-carbon:document-add
      href="/add"
      title="Add"
    />

    <a
      icon-btn i-carbon:image-search
      href="/search_prompt"
      title="Search By Prompt"
    />

    <a
      icon-btn i-carbon:tag-group
      href="/search_tag"
      title="Search By Tag"
    />

    <a
      icon-btn i-carbon:data-vis-1
      href="/tree"
      title="Tree"
    />

    <a
      icon-btn i-carbon:edit
      href="/edit"
      title="Edit"
    />

    <!-- <a
      icon-btn i-carbon:virtual-column-key
      href="/keys"
      title="Keys"
    />

    <a
      icon-btn i-carbon:settings-adjust
      href="/config"
      title="Config"
    /> -->

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
</template>
