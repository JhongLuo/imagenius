// util.ts
//
// This file contains a collection of utility functions that are used
// throughout the application.
//
//
export interface RawImageData {
  key: string
  src: string
}

export interface Image extends RawImageData {
  srcSaved: string
}

export type Selectable = { selected: boolean } & unknown

export type Labeled = { label: string } & unknown

export interface RawStatsData {
  timestamp: number[]
  miss_rate: number[]
  hit_rate: number[]
  nodes_num: number[]
  items_len: number[]
  items_bytes: number[]
  requests_count: number[]
}

export interface StatsData {
  nums_nodes: number[]
  hit_rates: number[]
  miss_rates: number[]
  nums_items: number[]
  usages_size: number[]
  nums_requests: number[]
}

export interface CacheConfigOptions {
  mode: string
  numNodes?: number
  cacheSize: number
  policy: string
  expRatio?: number
  shrinkRatio?: number
  maxMiss?: number
  minMiss?: number
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

  strAsNonNegNumber(str: string, min = 0, max?: number, isInclusive = true) {
    str = str.replace(/^0+|[^\d.]/g, '')
    if (max && min > max)
      return str
    if (Number(str) < min && isInclusive)
      return min.toString()
    if (Number(str) <= min && !isInclusive)
      return (min + 0.01).toString()
    if (max && Number(str) > max && isInclusive)
      return max.toString()
    if (max && Number(str) >= max && !isInclusive)
      return (max - 0.01).toString()
    else
      return str
  },
}
