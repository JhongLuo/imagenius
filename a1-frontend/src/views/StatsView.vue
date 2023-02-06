<template>
  <!--  Page Title  -->
  <div class="container mb-5">
    <h1>Cache Statistics</h1>
  </div>

  <!--  Page Content: Charts  -->
  <div class="container-lg px-0 mb-3">
    <div class="container">
      <button type="submit" class="btn btn-warning" @click="buttonPressed">
        Refresh
      </button>
    </div>

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
</template>

<script>
import { onMounted, ref, reactive } from "vue";
import { Chart } from "chart.js/auto";
import APIEndpoints from "@/services/APIEndpoints";
import utils from "@/composables/utils";
import * as Constants from "@/composables/constants";

export default {
  setup() {
    onMounted(() => {
      // mountCharts();
      // handleGetStats();
    });

    const stats = reactive({
      nums_items: [],
      usages_size: [],
      usages_percent: [],
      nums_requests: [],
      hit_rates: [],
      miss_rates: [],
    });
    const idChartNumsItems = ref("chart_nums_items");
    const idChartUsagesSize = ref("chart_usages_size");
    const idChartUsagesPercent = ref("chart_usages_percent");
    const idChartNumsRequests = ref("chart_nums_requests");
    const idChartHitRates = ref("chart_hit_rates");
    const idChartMissRates = ref("chart_miss_rates");

    const stateErrorMsg = ref("");
    const stateSuccessMsg = ref("");

    const chartNumsItems = reactive({});
    const chartUsageSize = reactive({});
    const chartUsagePercent = reactive({});
    const chartNumsRequests = reactive({});
    const chartHitRates = reactive({});
    const chartMissRates = reactive({});

    const mountCharts = () => {
      chartNumsItems.value = initChartByDOM(
        idChartNumsItems.value,
        "# of Items"
      );
      chartUsageSize.value = initChartByDOM(
        idChartUsagesSize.value,
        "Cache Usage (Size)"
      );
      chartUsagePercent.value = initChartByDOM(
        idChartUsagesPercent.value,
        "Cache Usage (Percentage)",
        "PERCENT"
      );
      chartNumsRequests.value = initChartByDOM(
        idChartNumsRequests.value,
        "Requests Served"
      );
      chartHitRates.value = initChartByDOM(
        idChartHitRates.value,
        "Hit Rate",
        "PERCENT"
      );
      chartMissRates.value = initChartByDOM(
        idChartMissRates.value,
        "Miss Rate",
        "PERCENT"
      );
    };

    const initChartByDOM = (id, title, type = "NUM") => {
      return new Chart(
        document.getElementById(id),
        utils.generateChartConfig(title, type)
      );
    };

    const updateCharts = () => {
      updateChart(chartNumsItems.value, stats.nums_items);
      updateChart(chartUsageSize.value, stats.usages_size);
      updateChart(chartUsagePercent.value, stats.usages_percent);
      updateChart(chartNumsRequests.value, stats.nums_requests);
      updateChart(chartHitRates.value, stats.hit_rates);
      updateChart(chartMissRates.value, stats.miss_rates);
    };

    const updateChart = (chart, dataArray) => {
      console.log("here start");
      chart.data.labels.push("");
      chart.data.datasets.forEach((dataset) => {
        dataset.data = dataArray;
      });
      chart.update();
      console.log("here end");
    };

    const populateStats = (data) => {
      for (let i = 0; i < data["max_size"].length; i++) {
        stats.nums_items.push(data["item_len"][i]);
        stats.usages_size.push(data["item_bytes"][i]);
        stats.usages_percent.push(data["item_bytes"][i] / data["max_size"][i]);
        stats.nums_requests.push(data["requests_count"][i]);
        stats.hit_rates.push(data["hit_rate"][i]);
        stats.miss_rates.push(data["miss_rate"][i]);
      }
    };

    const drawChart = () => {
      // chart DOMs
      const chart_nums_items = document.getElementById("chart_nums_items");
      const chart_sizes_occupied = document.getElementById(
        "chart_sizes_occupied"
      );
      const chart_percents_occupied = document.getElementById(
        "chart_percents_occupied"
      );
      const chart_nums_requests = document.getElementById(
        "chart_nums_requests"
      );
      const chart_hit_rates = document.getElementById("chart_hit_rates");
      const chart_miss_rates = document.getElementById("chart_miss_rates");
      // end DOMs

      new Chart(
        chart_nums_items,
        utils.renderChartConfig("# of Items", stats.nums_items, "NUM")
      );
      new Chart(
        chart_sizes_occupied,
        utils.renderChartConfig("Cache Usage (Size)", stats.usages_size, "NUM")
      );
      new Chart(
        chart_percents_occupied,
        utils.renderChartConfig(
          "Cache Usage (Percentage)",
          stats.usages_percent,
          "PERCENT"
        )
      );
      new Chart(
        chart_nums_requests,
        utils.renderChartConfig("Requests Served", stats.nums_requests, "NUM")
      );
      new Chart(
        chart_hit_rates,
        utils.renderChartConfig("Hit Rate", stats.hit_rates, "PERCENT")
      );
      new Chart(
        chart_miss_rates,
        utils.renderChartConfig("Miss Rate", stats.miss_rates, "PERCENT")
      );
    };

    const buttonPressed = () => {
      stats.nums_items.push(6);
      stats.usages_size.push(1048576);
      stats.usages_percent.push(0.6);
      stats.nums_requests.push(10);
      stats.hit_rates.push(0.8);
      stats.miss_rates.push(0.2);
      // drawChart();
      updateCharts();
    };

    const handleGetStats = async (ifSkipSuccessToast = false) => {
      // fetch data
      try {
        let response;
        response = await APIEndpoints.getStats();
        utils.helperThrowIfNotSuccess(response);
        // handle success
        const rawStats = utils.arrayOfObjsToObjOfArrays(response.data.stats);
        populateStats(rawStats);
        updateCharts();

        // console.log(stats.percents_occupied);
        if (!ifSkipSuccessToast) {
          stateSuccessMsg.value = Constants.SUCCESS_MSG_GET_KEYS;
          // utils.triggerToast(Constants.ID_TOAST_SUCCESS);
        }
      } catch (errMsg) {
        // handle error
        stateErrorMsg.value = errMsg;
        // utils.triggerToast(Constants.ID_TOAST_ERROR);
      }
    };

    return {
      stats,
      idChartNumsItems,
      idChartUsagesSize,
      idChartUsagesPercent,
      idChartNumsRequests,
      idChartHitRates,
      idChartMissRates,
      stateErrorMsg,
      stateSuccessMsg,
      handleGetStats,
      buttonPressed,
    };
  },
};
</script>

<style scoped></style>
