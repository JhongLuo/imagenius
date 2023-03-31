<script setup lang="ts">
const props = defineProps<{
  id: string
  title: string
  series: ApexAxisChartSeries
}>()

const isDark = useDark()

const yAxisLabelFormatter = (value: number) => {
  return `${value * 100}%`
}

const chartOptions = computed(() => {
  return {
    chart: {
      id: props.id,
      type: 'line',
      fontFamily: 'DM Sans',
      foreColor: isDark.value ? 'white' : 'black',
      redrawOnWindowResize: false,
      toolbar: {
        show: false,
      },
      zoom: {
        enabled: false,
      },
    },

    dataLabels: {
      enabled: false,
    },

    grid: {
      borderColor: isDark.value ? '#444444' : '#dddddd',
      row: {
        colors: [isDark.value ? '#444444' : '#dddddd',
          'transparent'],
        opacity: 0.1,
      },
    },

    legend: {
      show: false,
      showForSingleSeries: true,
      floating: true,
      fontSize: '16px',
      fontFamily: 'DM Sans',
      fontWeight: 1000,
      onItemClick: {
        toggleDataSeries: false,
      },
      onItemHover: {
        highlightDataSeries: true,
      },
    },

    markers: {
      size: 0,
      colors: undefined,
      strokeWidth: 1,
      strokeOpacity: 0.5,
      shape: 'circle',
      showNullDataPoints: true,
      hover: {
        size: 5,
      },
    },

    stroke: {
      show: true,
      curve: 'smooth',
      lineCap: 'round',
      colors: [isDark.value ? '#82E0AA' : '#73C797'],
      width: 4,
    },

    title: {
      text: props.title,
      style: {
        color: isDark.value ? 'white' : 'black',
        fontSize: '18px',
        fontFamily: 'DM Sans',
        fontWeight: 1000,
      },
    },

    tooltip: {
      enabled: true,
      followCursor: true,
      intersect: false,
      fillSeriesColor: false,
      theme: isDark.value ? 'dark' : 'light',
      style: {
        fontSize: '14px',
        fontFamily: 'DM Sans',
      },
    },

    xaxis: {
      labels: {
        show: false,
      },
      axisTicks: {
        show: false,
      },
      crosshairs: {
        show: false,
      },
      tooltip: {
        enabled: false,
      },
    },

    yaxis: {
      min: 0,
      max: 1,
      forceNiceScale: false,
      tickAmount: 4,
      decimalsInFloat: 2,
      labels: {
        show: true,
        formatter: yAxisLabelFormatter,
      },
    },

  } as ApexOptions
})
</script>

<template>
  <div>
    <apexchart
      :options="chartOptions"
      :series="series"
    />
  </div>
</template>
