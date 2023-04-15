import type { CacheConfigOptions } from './utils'

// toast: ids + messages
export const TOAST_ID__GENERATE_HINT__SUCCESS = 'toast-id-generate-hint-success'
export const TOAST_ID__GENERATE_HINT__ERROR = 'toast-id-generate-hint-error'
export const TOAST_ID__GENERATE_IMGS__SUCCESS = 'toast-id-generate-images-success'
export const TOAST_ID__GENERATE_IMGS__ERROR = 'toast-id-generate-images-error'
export const TOAST_ID__SAVE_IMGS__SUCCESS = 'toast-id-save-images-success'
export const TOAST_ID__SAVE_IMGS__ERROR = 'toast-id-save-images-error'
export const TOAST_ID__SEARCH_IMGS__SUCCESS = 'toast-id-search-images-success'
export const TOAST_ID__SEARCH_IMGS__ERROR = 'toast-id-search-images-error'
export const TOAST_ID__GET_TAGS__SUCCESS = 'toast-id-get-tags-success'
export const TOAST_ID__GET_TAGS__ERROR = 'toast-id-get-tags-error'
export const TOAST_ID__GET_ALL_IMGS__SUCCESS = 'toast-id-get-all-imgs-success'
export const TOAST_ID__GET_ALL_IMGS__ERROR = 'toast-id-get-all-imgs-error'
export const TOAST_ID__DELETE_ALL_IMGS__SUCCESS = 'toast-id-delete-all-imgs-success'
export const TOAST_ID__DELETE_ALL_IMGS__ERROR = 'toast-id-delete-all-imgs-error'
export const TOAST_ID__UPLOAD_IMG__SUCCESS = 'toast-id-upload-image-success'
export const TOAST_ID__UPLOAD_IMG__ERROR = 'toast-id-upload-image-error'
export const TOAST_ID__RETRIEVE_IMG__SUCCESS = 'toast-id-retrieve-image-success'
export const TOAST_ID__RETRIEVE_IMG__ERROR = 'toast-id-retrieve-image-error'
export const TOAST_ID__GET_ALL_KEYS__SUCCESS = 'toast-id-get-all-keys-success'
export const TOAST_ID__GET_ALL_KEYS__ERROR = 'toast-id-get-all-keys-error'
export const TOAST_ID__DELETE_ALL__SUCCESS = 'toast-id-delete-all-success'
export const TOAST_ID__DELETE_ALL__ERROR = 'toast-id-delete-all-error'
export const TOAST_ID__GET_CACHE_CONFIGS__SUCCESS = 'toast-id-get-cache-configs-success'
export const TOAST_ID__GET_CACHE_CONFIGS__ERROR = 'toast-id-get-cache-configs-error'
export const TOAST_ID__PUT_CACHE_CONFIGS__SUCCESS = 'toast-id-put-cache-configs-success'
export const TOAST_ID__PUT_CACHE_CONFIGS__ERROR = 'toast-id-put-cache-configs-error'
export const TOAST_ID__GET_CACHE_KEYS__SUCCESS = 'toast-id-get-cache-keys-success'
export const TOAST_ID__GET_CACHE_KEYS__ERROR = 'toast-id-get-cache-keys-error'
export const TOAST_ID__CLEAR_CACHE__SUCCESS = 'toast-id-clear-cache-success'
export const TOAST_ID__CLEAR_CACHE__ERROR = 'toast-id-clear-cache-error'
export const TOAST_ID__GET_STATS__SUCCESS = 'toast-id-get-stats-success'
export const TOAST_ID__GET_STATS__ERROR = 'toast-id-get-stats-error'
export const TOAST_ID__REFRESH_STATS__INFO = 'toast-id-refresh-stats-info'
export const TOAST_ID__GET_NUM_NODES__ERROR = 'toast-id-get-num-nodes-error'
export const TOAST_ID__NEW_NUM_NODES = 'toast-id-new-num-nodes'

export const TOAST_MSG__GENERATE_IMGS__SUCCESS = 'Imgs generated successfully.'
export const TOAST_MSG__SAVE_IMGS__SUCCESS = 'Images saved successfully.'
export const TOAST_MSG__SEARCH_IMGS__SUCCESS = 'Search results returned successfully.'
export const TOAST_MSG__GET_TAGS__SUCCESS = 'Tags loaded successfully.'
export const TOAST_MSG__GET_ALL_IMGS__SUCCESS = 'Imgs loaded successfully.'
export const TOAST_MSG__DELETE_ALL_IMGS__SUCCESS = 'Imgs deleted successfully.'
export const TOAST_MSG__UPLOAD_IMG__SUCCESS = 'Image uploaded successfully.'
export const TOAST_MSG__RETRIEVE_IMG__SUCCESS = 'Image retrieved successfully.'
export const TOAST_MSG__GET_ALL_KEYS__SUCCESS = 'Keys loaded successfully.'
export const TOAST_MSG__DELETE_ALL__SUCCESS = 'Data deleted successfully.'
export const TOAST_MSG__GET_CACHE_CONFIGS__SUCCESS = 'Cache configs loaded successfully.'
export const TOAST_MSG__PUT_CACHE_CONFIGS__SUCCESS = 'Cache configs updated successfully.'
export const TOAST_MSG__GET_CACHE_KEYS__SUCCESS = 'Cache keys loaded successfully.'
export const TOAST_MSG__CLEAR_CACHE__SUCCESS = 'Cache erased successfully.'
export const TOAST_MSG__GET_STATS__SUCCESS = 'Stats loaded successfully.'
export const TOAST_MSG__REFRESH_STATS__INFO = 'Stats refresh ongoing.'
export const TOAST_MSG__NEW_NUM_NODES = (from: number, to: number) => `Memcache pool size changed from ${from} to ${to}.`

// modal: ids + titles + descriptions
export const MODAL_ID__DELETE_ALL_IMGS = 'modal-delete-all-images'
export const MODAL_ID__DELETE_ALL = 'modal-delete-all-keys'
export const MODAL_ID__PUT_CACHE_CONFIGS = 'modal-put-cache-configs'
export const MODAL_ID__CLEAR_CACHE = 'modal-clear-cache'

export const MODAL_TITLE__DELETE_ALL_IMGS = 'Delete All Images'
export const MODAL_TITLE__DELETE_ALL = 'Delete All Keys and Images'
export const MODAL_TITLE__PUT_CACHE_CONFIGS = 'Update Cache Configurations'
export const MODAL_TITLE__CLEAR_CACHE = 'Clear Cache Data'

export const MODAL_DESCRIPTION__DELETE_ALL_IMGS = 'Are you sure you want to delete all images? All data will be permanently removed. This action cannot be undone.'
export const MODAL_DESCRIPTION__DELETE_ALL = 'Are you sure you want to delete all keys and their associated images? All data will be permanently removed. This action cannot be undone.'
export const MODAL_DESCRIPTION__PUT_CACHE_CONFIGS = (data: CacheConfigOptions) => {
  return data.mode === 'manual'

    ? `The following configurations will be set:

    Mode:               ${data.mode} ,
    Number of nodes:    ${data.numNodes} ,
    Max cache size:     ${data.cacheSize} MB ,
    Replacement policy: ${data.policy} .

    Proceed to submit?`
    : `The following configurations will be set:

    Mode:               ${data.mode} ,
    Max cache size:     ${data.cacheSize} MB ,
    Replacement policy: ${data.policy} ,
    Expand ratio:       ${data.expRatio} ,
    Shrink ratio:       ${data.shrinkRatio} ,
    Max miss rate:      ${data.maxMiss}% ,
    Min miss rate:      ${data.minMiss}% .

    Proceed to submit?`
}
export const MODAL_DESCRIPTION__CLEAR_CACHE = 'Are you sure you want to erase the cache data? \nData will be permanently removed, and the configuration will be reset. This action cannot be undone.'

// keys table: titles + descriptions + delete button texts
export const TABLE_TITLE__ALL_KEYS = 'All Keys'
export const TABLE_TITLE__CACHE_KEYS = 'Cache Keys'

export const TABLE_DESCRIPTION__ALL_KEYS = 'keys in database & mem-cache'
export const TABLE_DESCRIPTION__CACHE_KEYS = 'keys in mem-cache'

export const TABLE_DELETE_BUTTON_TEXT__ALL_KEYS = 'Delete All'
export const TABLE_DELETE_BUTTON_TEXT__CACHE_KEYS = 'Clear Cache'

// stat: labels
export const STATS_LABEL__NUMS_ITEMS = 'num of items'
export const STATS_LABEL__USAGES_SIZE = 'usage by size'
export const STATS_LABEL__USAGES_PERCENT = 'usage by percentage'
export const STATS_LABEL__NUMS_REQUESTS = 'num of requests'
export const STATS_LABEL__HIT_RATES = 'hit rates'
export const STATS_LABEL__MISS_RATES = 'miss rates'

// chart: Ids + titles
export const CHART_ID__NUMS_ITEMS = 'chart-nums-items'
export const CHART_ID__USAGES_SIZE = 'chart-usages-size'
export const CHART_ID__USAGES_PERCENT = 'chart-usages-percent'
export const CHART_ID__NUMS_REQUESTS = 'chart-nums-requests'
export const CHART_ID__HIT_RATES = 'chart-hit-rates'
export const CHART_ID__MISS_RATES = 'chart-miss-rates'
export const CHART_ID__NUMS_NODES = 'chart-nums-nodes'
export const CHART_ID__H_M_RATES = 'chart-hit-miss-rates'

export const CHART_TITLE__NUMS_ITEMS = '# of Items in Cache'
export const CHART_TITLE__USAGES_SIZE = 'Size of Items in Cache (MB)'
export const CHART_TITLE__USAGES_PERCENT = 'Usage by Percentage'
export const CHART_TITLE__NUMS_REQUESTS = '# of Requests Served'
export const CHART_TITLE__HIT_RATES = 'Hit Rate'
export const CHART_TITLE__MISS_RATES = 'Miss Rate'
export const CHART_TITLE__NUMS_NODES = '# of Active Nodes'
export const CHART_TITLE__H_M_RATES = 'Hit & Miss Rate'

// error messages
export const ERROR_MSG__INCORRECT_FORMAT = 'Incorrect response format.'
export const ERROR_MSG__UNKNOWN_ERR = 'Unknown Error.'
export const ERROR_MSG__KEYS_TABLE_EMPTY = 'No Keys Were Found.'
