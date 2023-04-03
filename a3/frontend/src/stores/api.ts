import { acceptHMRUpdate, defineStore } from 'pinia'

export const useAPIStore = defineStore('api', () => {
  // set up ipAddr
  const defaultAddr = 'localhost:5000'

  const ipAddr = reactive({
    addr: defaultAddr,
  })

  const storedIPAddr = localStorage.getItem('ipAddr')
  ipAddr.addr = storedIPAddr ? JSON.parse(storedIPAddr).addr : defaultAddr

  watch(
    ipAddr,
    (val) => {
      localStorage.setItem('ipAddr', JSON.stringify(val))
    },
    { deep: true },
  )

  // set up api key
  const defaultApiKey = ''

  const apiKey = ref(defaultApiKey)

  const storedApiKey = localStorage.getItem('apiKey')
  if (storedApiKey)
    apiKey.value = storedApiKey

  watch(
    apiKey,
    (val) => {
      localStorage.setItem('apiKey', val)
    },
  )

  // other variables
  const baseURL = computed(() => `http://${ipAddr.addr}/`)
  const baseURLShort = computed(() => `${ipAddr.addr}`)

  const baseAxios = computed(() => axios.create({ baseURL: baseURL.value }))

  // API CALLS:

  // - Update API Key:
  //
  const updateApiKey = () => baseAxios.value.post('/api/set_api_key', apiKey.value)

  // ADD PAGE
  // ----------------------------------------------------------------
  //

  // - Generate Images:
  //
  // request format:
  // (POST)
  //   {
  //     "prompt": String,
  //   }
  //
  // response format:
  //   {
  //     "success": "true",
  //     "images" : [Image]
  //   }
  //
  // image obj format:
  //   {
  //     "key": String,
  //     "url": String
  //   }
  //
  //
  const generateImages = (data: FormData) => baseAxios.value.post('/api/generate', data)

  // - Save Images:
  //
  // request format:
  // (POST)
  //   {
  //     "key_selections": JSON String of [String] # decode using json.loads()
  //   }
  //
  // response format:
  //   {
  //     "success": "true",
  //   }
  //
  //
  const saveImages = (data: FormData) => baseAxios.value.post('/api/save', data)

  // - Search Images:
  //
  // request format:
  // (POST)
  //   {
  //     "prompt": String,
  //   }
  //
  // response format:
  //   {
  //     "success": "true",
  //     "images" : [Image]
  //   }
  //
  // image obj format:
  //   {
  //     "key": String,
  //     "url": String
  //   }
  //
  //
  const searchImages = (data: FormData) => baseAxios.value.post('/api/search', data)

  return {
    ipAddr,
    apiKey,
    baseURLShort,
    updateApiKey,
    generateImages,
    saveImages,
    searchImages,
  }
})

if (import.meta.hot)
  import.meta.hot.accept(acceptHMRUpdate(useAPIStore, import.meta.hot))
