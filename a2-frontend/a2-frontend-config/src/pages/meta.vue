<script setup lang="ts">
defineOptions({
  name: 'MetaPage',
})

const api = useAPIStore()
const { toastsArray, blinkToast } = useToasts()

const isDownloadingRds = ref(false)
const isDownloadingManager = ref(false)
const isDownloadingScaler = ref(false)
const isDownloadingMemcache = ref(false)

const rdsConfigs = reactive({
  user: '',
  password: '',
  host: '',
  database: '',
})

const managerConfigs = reactive({
  ip: '',
  port: 0,
})

const scalerConfigs = reactive({
  ip: '',
  port: 0,
})

interface MemcacheConfig {
  ip: string
  port: number
}

const memcacheConfigsRef = ref<MemcacheConfig[]>([])

const initMemCacheConfigsRef = () => {
  for (let i = 0; i < 8; i++) {
    const newCopy = [...memcacheConfigsRef.value]
    newCopy.push({
      ip: '',
      port: 0,
    } as MemcacheConfig)
    memcacheConfigsRef.value = newCopy
  }
}

const getRds = async () => {
  isDownloadingRds.value = true
  try {
    const response = await api.getMetaConfigsRds()
    // handle success
    rdsConfigs.user = response.data.user
    rdsConfigs.password = response.data.password
    rdsConfigs.host = response.data.host
    rdsConfigs.database = response.data.database
    await utils.sleep(150)
    blinkToast(
      'toast-get-rds-success',
      'info',
      'RDS loaded.')
  }
  catch (err) {
    blinkToast(
      'toast-get-rds-error',
      'error',
      err as string)
  }
  finally {
    isDownloadingRds.value = false
  }
}

const getManager = async () => {
  isDownloadingManager.value = true
  try {
    const response = await api.getMetaConfigsManager()
    // handle success
    managerConfigs.ip = response.data.ip
    managerConfigs.port = response.data.port
    await utils.sleep(150)
    blinkToast(
      'toast-get-manager-success',
      'info',
      'Manager loaded.')
  }
  catch (err) {
    blinkToast(
      'toast-get-manager-error',
      'error',
      err as string)
  }
  finally {
    isDownloadingManager.value = false
  }
}

const getScaler = async () => {
  isDownloadingScaler.value = true
  try {
    const response = await api.getMetaConfigsScaler()
    // handle success
    scalerConfigs.ip = response.data.ip
    scalerConfigs.port = response.data.port
    await utils.sleep(150)
    blinkToast(
      'toast-get-scaler-success',
      'info',
      'Scaler loaded.')
  }
  catch (err) {
    blinkToast(
      'toast-get-scaler-error',
      'error',
      err as string)
  }
  finally {
    isDownloadingScaler.value = false
  }
}

const getMemcache = async () => {
  isDownloadingMemcache.value = true
  try {
    const response = await api.getMetaConfigsMemcache()
    // handle success
    memcacheConfigsRef.value = response.data.cache_config_list
    await utils.sleep(150)
    blinkToast(
      'toast-get-memcache-success',
      'info',
      'Memcache loaded.')
  }
  catch (err) {
    blinkToast(
      'toast-get-memcache-error',
      'error',
      err as string)
  }
  finally {
    isDownloadingMemcache.value = false
  }
}

const postRds = async () => {
  isDownloadingRds.value = true
  try {
    const data = {
      user: rdsConfigs.user,
      password: rdsConfigs.password,
      host: rdsConfigs.host,
      database: rdsConfigs.database,
    }
    const response = await api.postMetaConfigsRds(data)
    // handle success
    rdsConfigs.user = response.data.user
    rdsConfigs.password = response.data.password
    rdsConfigs.host = response.data.host
    rdsConfigs.database = response.data.database
    await utils.sleep(150)
    blinkToast(
      'toast-post-rds-success',
      'success',
      'RDS updated.')
  }
  catch (err) {
    blinkToast(
      'toast-post-rds-error',
      'error',
      err as string)
  }
  finally {
    isDownloadingRds.value = false
  }
}

const postManager = async () => {
  isDownloadingManager.value = true
  try {
    const data = {
      ip: managerConfigs.ip,
      port: managerConfigs.port,
    }
    const response = await api.postMetaConfigsManager(data)
    // handle success
    managerConfigs.ip = response.data.ip
    managerConfigs.port = response.data.port
    await utils.sleep(150)
    blinkToast(
      'toast-post-manager-success',
      'success',
      'Manager updated.')
  }
  catch (err) {
    blinkToast(
      'toast-post-manager-error',
      'error',
      err as string)
  }
  finally {
    isDownloadingManager.value = false
  }
}

const postScaler = async () => {
  isDownloadingScaler.value = true
  try {
    const data = {
      ip: scalerConfigs.ip,
      port: scalerConfigs.port,
    }
    const response = await api.postMetaConfigsScaler(data)
    // handle success
    scalerConfigs.ip = response.data.ip
    scalerConfigs.port = response.data.port
    await utils.sleep(150)
    blinkToast(
      'toast-post-scaler-success',
      'success',
      'Scaler updated.')
  }
  catch (err) {
    blinkToast(
      'toast-post-scaler-error',
      'error',
      err as string)
  }
  finally {
    isDownloadingScaler.value = false
  }
}

const postMemcache = async () => {
  isDownloadingMemcache.value = true
  try {
    const data = {
      cache_config_list: memcacheConfigsRef.value,
    }
    const response = await api.postMetaConfigsMemcache(data)
    // handle success
    memcacheConfigsRef.value = response.data.cache_config_list
    await utils.sleep(150)
    blinkToast(
      'toast-post-memcache-success',
      'success',
      'Memcache updated.')
  }
  catch (err) {
    blinkToast(
      'toast-post-memcache-error',
      'error',
      err as string)
  }
  finally {
    isDownloadingMemcache.value = false
  }
}

onMounted(() => {
  initMemCacheConfigsRef()
  getRds()
  getManager()
  getScaler()
  getMemcache()
})
</script>

<template>
  <!-- Page Title -->
  <h1 my-title>
    Meta Configs
  </h1>

  <!-- Page Content -->
  <div
    w-5xl
    flex flex-col justify-start items-center
    space-y-4
  >
    <!-- 1st row -->
    <div
      w-5xl
      flex flex-row justify-between items-start
      space-x-4
    >
      <!-- RDS -->
      <TheMetaCard
        :is-blurred="isDownloadingRds"
      >
        <h2>RDS</h2>
        <TheLabeledInput
          v-model="rdsConfigs.user"
          input-id="meta-rds-user"
          label-text="user"
          font-mono
        />
        <TheLabeledInput
          v-model="rdsConfigs.password"
          input-id="meta-rds-password"
          label-text="password"
          font-mono
        />
        <TheLabeledInput
          v-model="rdsConfigs.host"
          input-id="meta-rds-host"
          label-text="host"
          font-mono
        />
        <TheLabeledInput
          v-model="rdsConfigs.database"
          input-id="meta-rds-database"
          label-text="database"
          font-mono
        />
        <TheButton
          label="Save"
          :disabled="!rdsConfigs.user || !rdsConfigs.password || !rdsConfigs.host || !rdsConfigs.database"
          @click="postRds"
        />
      </TheMetaCard>

      <!-- Manger -->
      <TheMetaCard
        :is-blurred="isDownloadingManager"
      >
        <h2>Manger</h2>
        <TheLabeledInput
          v-model="managerConfigs.ip"
          input-id="meta-manager-ip"
          label-text="ip"
          font-mono
        />
        <TheLabeledInput
          v-model="managerConfigs.port"
          type="number"
          input-id="meta-manager-port"
          label-text="port"
          font-mono
        />
        <div />
        <TheButton
          label="Save"
          :disabled="!managerConfigs.ip || managerConfigs.port.toString() === ''"
          @click="postManager"
        />
      </TheMetaCard>

      <!-- Scaler -->
      <TheMetaCard
        :is-blurred="isDownloadingScaler"
      >
        <h2>Scaler</h2>
        <TheLabeledInput
          v-model="scalerConfigs.ip"
          input-id="meta-scaler-ip"
          label-text="ip"
          font-mono
        />
        <TheLabeledInput
          v-model="scalerConfigs.port"
          type="number"
          input-id="meta-scaler-port"
          label-text="port"
          font-mono
        />
        <TheButton
          label="Save"
          :disabled="!scalerConfigs.ip || scalerConfigs.port.toString() === ''"
          @click="postScaler"
        />
      </TheMetaCard>
    </div>

    <!-- 2nd row -->
    <TheMetaCard
      w-full
      :is-blurred="isDownloadingMemcache"
    >
      <h2 mb-8 text-lg>
        Memcache
      </h2>
      <div
        v-if="memcacheConfigsRef.length !== 0"
        w-full
        grid grid-cols-4
        gap-8
      >
        <div
          v-for="(_, index) in memcacheConfigsRef"
          :id="`memcache-${index}`"
          :key="index"
        >
          <h3>Cache {{ index + 1 }}</h3>
          <TheLabeledInput
            v-model="memcacheConfigsRef[index].ip"
            :input-id="`meta-memcache-ip-${index}`"
            label-text="ip"
            font-mono
          />
          <TheLabeledInput
            v-model="memcacheConfigsRef[index].port"
            type="number"
            :input-id="`meta-memcache-port-${index}`"
            label-text="port"
            font-mono
          />
        </div>
      </div>

      <div class="h-3" />

      <TheButton
        label="Save"
        :disabled="!memcacheConfigsRef.length"
        @click="postMemcache"
      />
    </TheMetaCard>
  </div>

  <!-- Toasts, Alerts & Modals -->
  <TheToasts
    :toasts-array="toastsArray"
  />
</template>
