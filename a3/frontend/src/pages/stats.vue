<script setup lang="ts">
defineOptions({
  name: 'StatsPage',
})

const api = useAPIStore()
const { toastsArray, blinkToast } = useToasts()

const stats = reactive<StatsData>({
  nums_nodes: [] as number[],
  hit_rates: [] as number[],
  miss_rates: [] as number[],
  nums_items: [] as number[],
  usages_size: [] as number[],
  nums_requests: [] as number[],
})

const populateStats = (rawData: RawStatsData) => {
  const newStatsData = {
    nums_nodes: [] as number[],
    hit_rates: [] as number[],
    miss_rates: [] as number[],
    nums_items: [] as number[],
    usages_size: [] as number[],
    nums_requests: [] as number[],
  } as StatsData

  for (let i = 0; i < rawData.timestamp.length; i++) {
    newStatsData.nums_nodes.push(rawData.nodes_num[i])
    newStatsData.hit_rates.push(rawData.hit_rate[i])
    newStatsData.miss_rates.push(rawData.miss_rate[i])
    newStatsData.nums_items.push(rawData.items_len[i])
    newStatsData.usages_size.push(rawData.items_bytes[i]) // raw data already in MB
    newStatsData.nums_requests.push(rawData.requests_count[i])
  }

  stats.nums_nodes = newStatsData.nums_nodes
  stats.hit_rates = newStatsData.hit_rates
  stats.miss_rates = newStatsData.miss_rates
  stats.nums_items = newStatsData.nums_items
  stats.usages_size = newStatsData.usages_size
  stats.nums_requests = newStatsData.nums_requests
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
    s_nums_nodes: [
      {
        name: STATS_LABEL__NUMS_ITEMS,
        data: stats.nums_nodes,
      }],

    s_h_m_rates: [
      {
        name: STATS_LABEL__HIT_RATES,
        data: stats.hit_rates,
      },
      {
        name: STATS_LABEL__MISS_RATES,
        data: stats.miss_rates,
      }],

    s_nums_items: [
      {
        name: STATS_LABEL__NUMS_ITEMS,
        data: stats.nums_items,
      }],

    s_usages_size: [
      {
        name: STATS_LABEL__USAGES_SIZE,
        data: stats.usages_size,
      }],

    s_nums_requests: [
      {
        name: STATS_LABEL__NUMS_REQUESTS,
        data: stats.nums_requests,
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
    <TheChartNumsNodes
      v-if="stats.nums_nodes.length"
      :id="CHART_ID__NUMS_NODES"
      :title="CHART_TITLE__NUMS_NODES"
      :series="statsSeries.s_nums_nodes"
    />

    <TheChartHMRates
      v-if="stats.hit_rates.length"
      :id="CHART_ID__H_M_RATES"
      :title="CHART_TITLE__H_M_RATES"
      :series="statsSeries.s_h_m_rates"
    />

    <TheChartNumsItems
      v-if="stats.nums_items.length"
      :id="CHART_ID__NUMS_ITEMS"
      :title="CHART_TITLE__NUMS_ITEMS"
      :series="statsSeries.s_nums_items"
    />

    <TheChartUsagesSize
      v-if="stats.usages_size.length"
      :id="CHART_ID__USAGES_SIZE"
      :title="CHART_TITLE__USAGES_SIZE"
      :series="statsSeries.s_usages_size"
    />

    <TheChartNumsRequests
      v-if="stats.nums_requests.length"
      :id="CHART_ID__NUMS_REQUESTS"
      :title="CHART_TITLE__NUMS_REQUESTS"
      :series="statsSeries.s_nums_requests"
    />
  </TheStatsGrid>

  <!-- Toasts, Alerts & Modals -->
  <TheToasts
    :toasts-array="toastsArray"
  />
</template>
