export default {
  helperThrowIfNotSuccess(response) {
    if (response.data.success == false) throw "failure";
  },
};
