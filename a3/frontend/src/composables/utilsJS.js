// utilJS.js
//
// This file contains some utility functions for non-typed
// scenarios.
//
import * as Constants from '~/composables/constants'

export default {
  validateResponse(response) {
    // wrong response format
    const noSuccessKey = !('success' in response.data)
    if (noSuccessKey)
      throw Constants.ERROR_MSG__INCORRECT_FORMAT

    const invalidSuccessVal = !(
      response.data.success === 'true' || response.data.success === 'false'
    )
    if (invalidSuccessVal)
      throw Constants.ERROR_MSG__INCORRECT_FORMAT

    // <NO ERROR>
    if (response.data.success === 'true')
      return

    // wrong response format
    const failButNoError = !('error' in response.data)
    if (failButNoError)
      throw Constants.ERROR_MSG__INCORRECT_FORMAT

    const errorIsNotObjOrEmpty
      = typeof response.data.error !== 'object' || response.data.error === null
    if (errorIsNotObjOrEmpty)
      throw Constants.ERROR_MSG__INCORRECT_FORMAT

    const failButNoErrorMsg = !('message' in response.data.error)
    if (failButNoErrorMsg)
      throw Constants.ERROR_MSG__INCORRECT_FORMAT

    // unknown error: error msg is not string
    const messageIsNotStr = typeof response.data.error.message !== 'string'
    if (messageIsNotStr)
      throw Constants.ERROR_MSG__UNKNOWN_ERR

    // throw responded error
    throw response.data.error.message
  },

  arrayOfObjsToObjOfArrays(statsArray) {
    const statsData = {}
    statsArray.forEach((timestamp) => {
      Object.keys(timestamp).forEach((key) => {
        if (statsData[key])
          statsData[key].push(timestamp[key])
        else
          statsData[key] = [timestamp[key]]
      })
    })

    return statsData
  },
}
