import * as bootstrap from "bootstrap";
import * as Constants from "@/composables/constants";

export default {
  helperThrowIfNotSuccess(response) {
    // wrong response format
    const noSuccessKey = !("success" in response.data);
    if (noSuccessKey) throw Constants.ERR_MSG_INCORRECT_FORMAT;

    const invalidSuccessVal = !(
      response.data.success === "true" || response.data.success === "false"
    );
    if (invalidSuccessVal) throw Constants.ERR_MSG_INCORRECT_FORMAT;

    // <NO ERROR>
    if (response.data.success === "true") return;

    // wrong response format
    const failButNoError = !("error" in response.data);
    if (failButNoError) throw Constants.ERR_MSG_INCORRECT_FORMAT;

    const errorIsNotObjOrEmpty =
      typeof response.data.error !== "object" || response.data.error === null;
    if (errorIsNotObjOrEmpty) throw Constants.ERR_MSG_INCORRECT_FORMAT;

    const failButNoErrorMsg = !("message" in response.data.error);
    if (failButNoErrorMsg) throw Constants.ERR_MSG_INCORRECT_FORMAT;

    // unknown error: error msg is not string
    const messageIsNotStr = typeof response.data.error.message !== "string";
    if (messageIsNotStr) throw Constants.ERR_MSG_UNKNOWN_ERROR;

    // throw responded error
    throw response.data.error.message;
  },

  triggerToast(toastID) {
    const toastError = document.getElementById(toastID);
    const toast = new bootstrap.Toast(toastError);
    toast.show();
  },
};
