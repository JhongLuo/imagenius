export default {
  helperThrowIfNotSuccess(response) {
    if (response.data.success !== "true") throw "failure";
  },
};
