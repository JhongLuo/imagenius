// util.ts
//
// This file contains a collection of utility functions that are used
// throughout the application.
//
//

export interface Node {
  name: string
  key: string
  src: string
  prompt: string
}

export interface Edge {
  source: string
  target: string
}

export interface RawImageData {
  key: string
  src: string
}

export interface Image extends RawImageData {
  srcSaved: string
}

export type Selectable = { selected: boolean } & unknown

export type Labeled = { label: string } & unknown

export interface EditConfigOptions {
  xPos: number
  yPos: number
  radius: number
  prompt: string
}

export interface RawStatsData {
  timestamp: number[]
  cache_size: number[]
  total_images: number[]
  total_tags: number[]
  total_prompt: number[]
  total_usage: number[]
}

export interface StatsData {
  nums_imgs_discarded: number[]
  nums_imgs_saved: number[]
  nums_tags: number[]
  nums_api_calls: number[]
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
  navigateToListAll() {
    window.location.href = '/list'
  },

  navigateToTree(key: string) {
    window.location.href = `/tree?key=${key}`
  },

  navigateToEdit(key: string) {
    window.location.href = `/edit?key=${key}`
  },

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
