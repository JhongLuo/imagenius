<script setup lang="ts">
defineOptions({
  name: 'StatsPage',
})

const api = useAPIStore()
const { toastsArray, blinkToast } = useToasts()

const stats = reactive({
  nums_items: [] as number[],
  nums_requests: [] as number[],
  usages_size: [] as number[],
  usages_percent: [] as number[],
  hit_rates: [] as number[],
  miss_rates: [] as number[],
} as StatsData)

const populateStats = (data: RawStatsData) => {
  const newStatsData = {
    nums_items: [] as number[],
    nums_requests: [] as number[],
    usages_size: [] as number[],
    usages_percent: [] as number[],
    hit_rates: [] as number[],
    miss_rates: [] as number[],
  } as StatsData

  for (let i = 0; i < data.max_size.length; i++) {
    newStatsData.nums_items.push(data.items_len[i])
    newStatsData.nums_requests.push(data.requests_count[i])
    newStatsData.usages_size.push(data.items_bytes[i] / (1024 ** 2))
    newStatsData.usages_percent.push(data.items_bytes[i] / data.max_size[i])
    newStatsData.hit_rates.push(data.hit_rate[i])
    newStatsData.miss_rates.push(data.miss_rate[i])
  }
  stats.nums_items = newStatsData.nums_items
  stats.nums_requests = newStatsData.nums_requests
  stats.usages_size = newStatsData.usages_size
  stats.usages_percent = newStatsData.usages_percent
  stats.hit_rates = newStatsData.hit_rates
  stats.miss_rates = newStatsData.miss_rates
}

const handleGetStats = async (ifReload = false) => {
  // fetch data
  try {
    const response = await api.getStats()
    utilsJS.validateResponse(response)
    // handle success
    const rawStatsData = utilsJS.arrayOfObjsToObjOfArrays(response.data.stats)
    populateStats(rawStatsData as RawStatsData)
    if (!ifReload) {
      blinkToast(
        TOAST_ID__GET_STATS__SUCCESS,
        'success',
        TOAST_MSG__GET_STATS__SUCCESS)
    }
  }
  catch (errMsg) {
    // handle error
    blinkToast(
      TOAST_ID__GET_STATS__ERROR,
      'error',
      errMsg as string)
  }
}

const isRefreshConfirmed = ref(false)

const handleRefreshStats = async () => {
  await utils.sleep(5000)

  while (true) {
    if (!isRefreshConfirmed.value) {
      isRefreshConfirmed.value = true
      blinkToast(
        TOAST_ID__REFRESH_STATS__INFO,
        'info',
        TOAST_MSG__REFRESH_STATS__INFO)
    }
    // refresh every 5 seconds
    await utils.sleep(5000)
    // fetch data
    try {
      const response = await api.getStats()
      utilsJS.validateResponse(response)
      // handle success
      const rawStatsData: RawStatsData = utilsJS.arrayOfObjsToObjOfArrays(response.data.stats)
      populateStats(rawStatsData as RawStatsData)
    }
    catch (errMsg) {
    // handle error
      blinkToast(
        TOAST_ID__GET_STATS__ERROR,
        'error',
        errMsg as string)
    }
  }
}

const statsSeries = computed(() => {
  return {
    nums_items: [{
      name: STATS_LABEL__NUMS_ITEMS,
      data: stats.nums_items,
    }],
    nums_requests: [{
      name: STATS_LABEL__NUMS_REQUESTS,
      data: stats.nums_requests,
    }],
    usages_size: [{
      name: STATS_LABEL__USAGES_SIZE,
      data: stats.usages_size,
    }],
    usages_percent: [{
      name: STATS_LABEL__USAGES_PERCENT,
      data: stats.usages_percent,
    }],
    hit_rates: [{
      name: STATS_LABEL__HIT_RATES,
      data: stats.hit_rates,
    }],
    miss_rates: [{
      name: STATS_LABEL__MISS_RATES,
      data: stats.miss_rates,
    }],
  }
})

onMounted(() => {
  handleGetStats()
  handleRefreshStats()
})
</script>

<template>
  <!-- Page Title -->
  <h1 my-title mb-12>
    Stats
  </h1>

  <!-- Page Content：Grid -->
  <TheStatsGrid>
    <TheChartNumsItems
      v-if="statsSeries.nums_items.length"
      :id="CHART_ID__NUMS_ITEMS"
      :title="CHART_TITLE__NUMS_ITEMS"
      :series="statsSeries.nums_items"
    />

    <TheChartNumsRequests
      v-if="statsSeries.nums_requests.length"
      :id="CHART_ID__NUMS_REQUESTS"
      :title="CHART_TITLE__NUMS_REQUESTS"
      :series="statsSeries.nums_requests"
    />

    <TheChartUsagesSize
      v-if="statsSeries.usages_size.length"
      :id="CHART_ID__USAGES_SIZE"
      :title="CHART_TITLE__USAGES_SIZE"
      :series="statsSeries.usages_size"
    />

    <TheChartUsagesPercent
      v-if="statsSeries.usages_percent.length"
      :id="CHART_ID__USAGES_PERCENT"
      :title="CHART_TITLE__USAGES_PERCENT"
      :series="statsSeries.usages_percent"
    />

    <TheChartHitRates
      v-if="statsSeries.hit_rates.length"
      :id="CHART_ID__HIT_RATES"
      :title="CHART_TITLE__HIT_RATES"
      :series="statsSeries.hit_rates"
    />

    <TheChartMissRates
      v-if="statsSeries.miss_rates.length"
      :id="CHART_ID__MISS_RATES"
      :title="CHART_TITLE__MISS_RATES"
      :series="statsSeries.miss_rates"
    />
  </TheStatsGrid>

  <!-- Toasts, Alerts & Modals -->
  <TheToasts
    :toasts-array="toastsArray"
  />
</template>
