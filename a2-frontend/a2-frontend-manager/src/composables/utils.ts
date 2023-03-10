// util.ts
//
// This file contains a collection of utility functions that are used
// throughout the application.
//
//
export interface RawStatsData {
  items_len: number[]
  requests_count: number[]
  items_bytes: number[]
  max_size: number[]
  hit_rate: number[]
  miss_rate: number[]
}

export interface StatsData {
  nums_items: number[]
  nums_requests: number[]
  usages_size: number[]
  usages_percent: number[]
  hit_rates: number[]
  miss_rates: number[]
}

export interface CacheConfigOptions {
  mode: string
  numNodes: number
  cacheSize: number
  policy: string
  expRatio: number
  shrinkRatio: number
  maxMiss: number
  minMiss: number
}

export default {
  sleep(ms = 500) {
    return new Promise(resolve => setTimeout(resolve, ms))
  },

  computeYAxisRange(array: number[]) {
    return {
      yAxisMin: this.computeYAxisMin(array),
      yAxisMax: this.computeYAxisMax(array),
    }
  },

  computeYAxisMin(array: number[]) {
    if (array.length === 0)
      return 0

    const minY = Math.min(...array)
    if (minY < 100)
      return 0
    else
      return Math.floor(minY / 100) * 100
  },

  computeYAxisMax(array: number[]) {
    if (array.length === 0)
      return 0

    const maxY = Math.max(...array)
    if (maxY < 10)
      return 10
    if (maxY < 100)
      return Math.ceil(maxY / 10) * 10
    else
      return Math.ceil(maxY / 100) * 100
  },
}
