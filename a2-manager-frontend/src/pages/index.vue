<script setup lang="ts" generic="T extends any, O extends any">
defineOptions({
  name: 'IndexPage',
})

const name = ref('')

// const router = useRouter()
const pressed = () => {
  // if (name)
  //   router.push(`/hi/${encodeURIComponent(name)}`)
  console.warn(name.value)
}
</script>

<template>
  <div>
    <TheInput
      v-model="name"
      placeholder="Where to connect?"
      autocomplete="false"
      @keydown.enter="pressed"
    />

    <div>
      <button
        class="m-3 text-sm btn"
        :disabled="!name"
        @click="pressed"
      >
        Go
      </button>
    </div>
  </div>
</template>
