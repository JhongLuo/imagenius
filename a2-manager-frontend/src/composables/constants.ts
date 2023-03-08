// toast ids
export const TOAST_ID_SUCCESS_UPLOAD_IMG = 'toast-success-upload-image'
export const TOAST_ID_ERROR_UPLOAD_IMG = 'toast-error-upload-image'
export const TOAST_ID_SUCCESS_RETRIEVE_IMG = 'toast-success-retrieve-image'
export const TOAST_ID_ERROR_RETRIEVE_IMG = 'toast-error-retrieve-image'
export const TOAST_ID_SUCCESS_GET_ALL_KEYS = 'toast-success-get-all-keys'
export const TOAST_ID_ERROR_GET_ALL_KEYS = 'toast-error-get-all-keys'
export const TOAST_ID_SUCCESS_DELETE_ALL = 'toast-success-delete-all'
export const TOAST_ID_ERROR_DELETE_ALL = 'toast-error-delete-all'
export const TOAST_ID_SUCCESS_GET_CACHE_CONFIGS = 'toast-success-get-cache-configs'
export const TOAST_ID_ERROR_GET_CACHE_CONFIGS = 'toast-error-get-cache-configs'
export const TOAST_ID_SUCCESS_PUT_CACHE_CONFIGS = 'toast-success-put-cache-configs'
export const TOAST_ID_ERROR_PUT_CACHE_CONFIGS = 'toast-error-put-cache-configs'
export const TOAST_ID_SUCCESS_GET_CACHE_KEYS = 'toast-success-get-cache-keys'
export const TOAST_ID_ERROR_GET_CACHE_KEYS = 'toast-error-get-cache-keys'
export const TOAST_ID_SUCCESS_CLEAR_CACHE = 'toast-success-clear-cache'
export const TOAST_ID_ERROR_CLEAR_CACHE = 'toast-error-clear-cache'

// toast success messages
export const MSG_SUCCESS_UPLOAD_IMG = 'Image uploaded successfully.'
export const MSG_SUCCESS_RETRIEVE_IMG = 'Image retrieved successfully.'
export const MSG_SUCCESS_GET_ALL_KEYS = 'Keys loaded successfully.'
export const MSG_SUCCESS_DELETE_ALL = 'Data deleted successfully.'
export const MSG_SUCCESS_GET_CACHE_CONFIGS = 'Cache configs loaded successfully.'
export const MSG_SUCCESS_PUT_CACHE_CONFIGS = 'Cache configs updated successfully.'
export const MSG_SUCCESS_GET_CACHE_KEYS = 'Cache keys loaded successfully.'
export const MSG_SUCCESS_CLEAR_CACHE = 'Cache erased successfully.'

// toast error messages
export const MSG_ERROR_INCORRECT_FORMAT = 'Incorrect response format.'
export const MSG_ERROR_UNKNOWN_ERR = 'Unknown Error.'
export const MSG_ERROR_KEYS_TABLE_EMPTY = 'No Keys Were Found.'

// modal ids and texts
export const MODAL_ID_DELETE_ALL = 'modal-delete-all-keys'
export const MODAL_TITLE_DELETE_ALL = 'Delete All Keys and Images'
export const MODAL_DESCRIPTION_DELETE_ALL = 'Are you sure you want to delete all keys and associated images? All of the data will be permanently removed. This action cannot be undone.'
export const MODAL_ID_PUT_CACHE_CONFIGS = 'modal-put-cache-configs'
export const MODAL_TITLE_PUT_CACHE_CONFIGS = 'Update Cache Configurations'
export const MODAL_DESCRIPTION_PUT_CACHE_CONFIGS = (replacementPolicy: string, maxSize: number) => `The new configurations will be: \nReplacement Policy: ${replacementPolicy}, \nMax Cache Size = ${maxSize} MB.`
export const MODAL_ID_CLEAR_CACHE = 'modal-clear-cache'
export const MODAL_TITLE_CLEAR_CACHE = 'Clear Cache Data'
export const MODAL_DESCRIPTION_CLEAR_CACHE = 'Are you sure you want to erase the cache data? \nData will be permanently removed, and the configuration will be reset. This action cannot be undone.'

// keys table titles, descriptions, and delete button text
export const TABLE_TITLE_ALL_KEYS = 'All Keys'
export const TABLE_DESCRIPTION_ALL_KEYS = 'keys in database & mem-cache'
export const TABLE_DELETE_BUTTON_TEXT_ALL_KEYS = 'Delete All'
export const TABLE_TITLE_CACHE_KEYS = 'Cache Keys'
export const TABLE_DESCRIPTION_CACHE_KEYS = 'keys in mem-cache'
export const TABLE_DELETE_BUTTON_TEXT_CACHE_KEYS = 'Clear Cache'
