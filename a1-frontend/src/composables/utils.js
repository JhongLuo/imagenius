import * as bootstrap from "bootstrap";
import * as Constants from "@/composables/constants";
// import { Chart } from "chart.js/auto";

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

  arrayOfObjsToObjOfArrays(statsArray) {
    const statsData = {};
    statsArray.forEach((timestamp) => {
      Object.keys(timestamp).forEach((key) => {
        if (statsData[key]) {
          statsData[key].push(timestamp[key]);
        } else {
          statsData[key] = [timestamp[key]];
        }
      });
    });

    return statsData;
  },

  generateChartConfig(title, array, numOrPercent = "NUM") {
    let scaleOptions;
    if (numOrPercent === "NUM") {
      scaleOptions = {
        x: {
          display: false,
        },
        y: {
          beginAtZero: true,
          grid: {
            tickLength: 2,
          },
          ticks: {
            precision: 0,
          },
        },
      };
    } else {
      scaleOptions = {
        x: {
          display: false,
        },
        y: {
          beginAtZero: true,
          suggestedMax: 1,
          grid: {
            tickLength: 2,
          },
          ticks: {
            stepSize: 0.25,
            callback: (value) => {
              return (value * 100).toFixed(0) + "%"; // convert it to percentage
            },
          },
        },
      };
    }

    const config = {
      type: "line",
      data: {
        labels: array,
        datasets: [
          {
            label: "",
            data: array,
            borderColor: "#82E0AA",
            borderWidth: 2,
          },
        ],
      },
      options: {
        responsive: true,
        plugins: {
          title: {
            display: true,
            text: title,
          },
          legend: {
            display: false,
          },
        },
        scales: scaleOptions,
      },
    };

    return config;
  },
};
