<script setup lang="ts">
import type { RawStatsData, StatsData } from '~/composables/utils'

defineOptions({
  name: 'StatsPage',
})

const api = useAPIStore()
const { toastsArray, blinkToast } = useToasts()

const stats = reactive<StatsData>({
  nums_imgs_discarded: [] as number[],
  nums_imgs_saved: [] as number[],
  nums_tags: [] as number[],
  nums_api_calls: [] as number[],
})

const populateStats = (rawData: RawStatsData) => {
  const newStatsData = {
    nums_imgs_discarded: [] as number[],
    nums_imgs_saved: [] as number[],
    nums_tags: [] as number[],
    nums_api_calls: [] as number[],
  } as StatsData

  for (let i = 0; i < rawData.timestamp.length; i++) {
    newStatsData.nums_imgs_discarded.push(rawData.cache_size[i])
    newStatsData.nums_imgs_saved.push(rawData.total_images[i])
    newStatsData.nums_tags.push(rawData.total_tags[i])
    newStatsData.nums_api_calls.push(rawData.total_usage[i])
  }

  stats.nums_imgs_discarded = newStatsData.nums_imgs_discarded
  stats.nums_imgs_saved = newStatsData.nums_imgs_saved
  stats.nums_tags = newStatsData.nums_tags
  stats.nums_api_calls = newStatsData.nums_api_calls
}

const handleGetStats = async (ifReload = false) => {
  // fetch data
  try {
    const response = await api.getStats()
    utilsJS.validateResponse(response)
    // handle success
    const rawStatsData = utilsJS.arrayOfObjsToObjOfArrays(response.data.stats) as RawStatsData
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
      const rawStatsData = utilsJS.arrayOfObjsToObjOfArrays(response.data.stats) as RawStatsData
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
    s_nums_imgs_discarded: [
      {
        name: STATS_LABEL__NUMS_IMGS_DISCARDED,
        data: stats.nums_imgs_discarded,
      }],

    s_nums_imgs_saved: [
      {
        name: STATS_LABEL__NUMS_IMGS_SAVED,
        data: stats.nums_imgs_saved,
      }],

    s_nums_tags: [
      {
        name: STATS_LABEL__NUMS_TAGS,
        data: stats.nums_tags,
      }],

    s_nums_api_calls: [
      {
        name: STATS_LABEL__NUMS_API_CALLS,
        data: stats.nums_api_calls,
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
    <TheChartNumsImgsDiscarded
      v-if="stats.nums_imgs_discarded.length"
      :id="CHART_ID__NUMS_IMGS_DISCARDED"
      :title="CHART_TITLE__NUMS_IMGS_DISCARDED"
      :series="statsSeries.s_nums_imgs_discarded"
    />

    <TheChartNumsImgsSaved
      v-if="stats.nums_imgs_saved.length"
      :id="CHART_ID__NUMS_IMGS_SAVED"
      :title="CHART_TITLE__NUMS_IMGS_SAVED"
      :series="statsSeries.s_nums_imgs_saved"
    />

    <TheChartNumsTags
      v-if="stats.nums_tags.length"
      :id="CHART_ID__NUMS_TAGS"
      :title="CHART_TITLE__NUMS_TAGS"
      :series="statsSeries.s_nums_tags"
    />

    <TheChartNumsApiCalls
      v-if="stats.nums_api_calls.length"
      :id="CHART_ID__NUMS_API_CALLS"
      :title="CHART_TITLE__NUMS_API_CALLS"
      :series="statsSeries.s_nums_api_calls"
    />
  </TheStatsGrid>

  <!-- Toasts, Alerts & Modals -->
  <TheToasts
    :toasts-array="toastsArray"
  />
</template>
