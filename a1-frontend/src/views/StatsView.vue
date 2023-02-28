<template>
  <!--  Page Title  -->
  <div class="container mb-5">
    <h1>Cache Statistics</h1>
  </div>

  <!--  Page Content: Charts  -->
  <div class="container-lg my-5 px-0 mb-3">
    <div class="container">
      <div class="row row-cols-2 g-5">
        <div class="col">
          <canvas :id="idChartNumsItems"></canvas>
        </div>
        <div class="col">
          <canvas :id="idChartUsagesSize"></canvas>
        </div>
        <div class="col">
          <canvas :id="idChartUsagesPercent"></canvas>
        </div>
        <div class="col">
          <canvas :id="idChartNumsRequests"></canvas>
        </div>
        <div class="col">
          <canvas :id="idChartHitRates"></canvas>
        </div>
        <div class="col">
          <canvas :id="idChartMissRates"></canvas>
        </div>
      </div>
    </div>
  </div>

  <!--  toasts  -->
  <div class="toast-container position-fixed bottom-0 end-0 p-3">
    <!--  error toast  -->
    <div
      id="errorToast"
      class="toast text-bg-danger"
      role="alert"
      aria-live="assertive"
      aria-atomic="true"
    >
      <div class="toast-header">
        <strong class="me-auto">ERROR</strong>
        <small>{{ storeAPI.baseURLShort }}</small>
        <button
          type="button"
          class="btn-close"
          data-bs-dismiss="toast"
          aria-label="Close"
        ></button>
      </div>
      <div class="toast-body">{{ stateErrorMsg }}</div>
    </div>

    <!--  success toast  -->
    <div
      id="successToast"
      class="toast text-bg-success"
      role="alert"
      aria-live="assertive"
      aria-atomic="true"
    >
      <div class="toast-header">
        <strong class="me-auto">SUCCESS</strong>
        <small>{{ storeAPI.baseURLShort }}</small>
        <button
          type="button"
          class="btn-close"
          data-bs-dismiss="toast"
          aria-label="Close"
        ></button>
      </div>
      <div class="toast-body">{{ stateSuccessMsg }}</div>
    </div>
  </div>
</template>

<script>
import { onMounted, reactive, ref } from "vue";
import Chart from "chart.js/auto";
import utils from "@/composables/utils";
import * as Constants from "@/composables/constants";
import { useAPIStore } from "@/stores/api";

export default {
  setup() {
    onMounted(() => {
      handleGetStats();
    });

    const storeAPI = useAPIStore();

    const stateErrorMsg = ref("");
    const stateSuccessMsg = ref("");

    const idChartNumsItems = ref("chart_nums_items");
    const idChartUsagesSize = ref("chart_usages_size");
    const idChartUsagesPercent = ref("chart_usages_percent");
    const idChartNumsRequests = ref("chart_nums_requests");
    const idChartHitRates = ref("chart_hit_rates");
    const idChartMissRates = ref("chart_miss_rates");

    const chartNumsItems = ref(null);
    const chartUsagesSize = ref(null);
    const chartUsagesPercent = ref(null);
    const chartNumsRequests = ref(null);
    const chartHitRates = ref(null);
    const chartMissRates = ref(null);

    const stats = reactive({
      nums_items: [],
      usages_size: [],
      usages_percent: [],
      nums_requests: [],
      hit_rates: [],
      miss_rates: [],
    });

    const titles = {
      nums_items: "# of Items",
      usages_size: "Cache Usage (size in MB)",
      usages_percent: "Cache Usage (percentage)",
      nums_requests: "Requests Served",
      hit_rates: "Hit Rate",
      miss_rates: "Miss Rate",
    };

    const drawCharts = () => {
      const configNumsItems = utils.generateChartConfig(
        titles.nums_items,
        stats.nums_items
      );
      const configUsagesSize = utils.generateChartConfig(
        titles.usages_size,
        stats.usages_size
      );
      const configUsagesPercent = utils.generateChartConfig(
        titles.usages_percent,
        stats.usages_percent,
        "PERCENT"
      );
      const configNumsRequests = utils.generateChartConfig(
        titles.nums_requests,
        stats.nums_requests
      );
      const configHitRates = utils.generateChartConfig(
        titles.hit_rates,
        stats.hit_rates,
        "PERCENT"
      );
      const configMissRates = utils.generateChartConfig(
        titles.miss_rates,
        stats.miss_rates,
        "PERCENT"
      );

      const DOMNumsItems = document.getElementById(idChartNumsItems.value);
      const DOMUsagesSize = document.getElementById(idChartUsagesSize.value);
      const DOMUsagesPercent = document.getElementById(
        idChartUsagesPercent.value
      );
      const DOMNumsRequests = document.getElementById(
        idChartNumsRequests.value
      );
      const DOMHitRates = document.getElementById(idChartHitRates.value);
      const DOMMissRates = document.getElementById(idChartMissRates.value);

      chartNumsItems.value = new Chart(DOMNumsItems, configNumsItems);
      chartUsagesSize.value = new Chart(DOMUsagesSize, configUsagesSize);
      chartUsagesPercent.value = new Chart(
        DOMUsagesPercent,
        configUsagesPercent
      );
      chartNumsRequests.value = new Chart(DOMNumsRequests, configNumsRequests);
      chartHitRates.value = new Chart(DOMHitRates, configHitRates);
      chartMissRates.value = new Chart(DOMMissRates, configMissRates);
    };

    const handleGetStats = async (ifSkipSuccessToast = false) => {
      // fetch data
      try {
        let response;
        response = await storeAPI.getStats();
        utils.helperThrowIfNotSuccess(response);
        // handle success
        const rawStats = utils.arrayOfObjsToObjOfArrays(response.data.stats);
        populateStats(rawStats);
        drawCharts();
        if (!ifSkipSuccessToast) {
          stateSuccessMsg.value = Constants.SUCCESS_MSG_GET_KEYS;
          utils.triggerToast(Constants.ID_TOAST_SUCCESS);
        }
      } catch (errMsg) {
        // handle error
        stateErrorMsg.value = errMsg;
        utils.triggerToast(Constants.ID_TOAST_ERROR);
      }
    };

    const populateStats = (data) => {
      for (let i = 0; i < data["max_size"].length; i++) {
        stats.nums_items.push(data["items_len"][i]);
        stats.usages_size.push(data["items_bytes"][i] / (1024 * 1024));
        stats.usages_percent.push(data["items_bytes"][i] / data["max_size"][i]);
        stats.nums_requests.push(data["requests_count"][i]);
        stats.hit_rates.push(data["hit_rate"][i]);
        stats.miss_rates.push(data["miss_rate"][i]);
      }
    };

    return {
      storeAPI,
      idChartNumsItems,
      idChartUsagesSize,
      idChartUsagesPercent,
      idChartNumsRequests,
      idChartHitRates,
      idChartMissRates,
      stateErrorMsg,
      stateSuccessMsg,
      handleGetStats,
    };
  },
};
</script>

<style scoped></style>
