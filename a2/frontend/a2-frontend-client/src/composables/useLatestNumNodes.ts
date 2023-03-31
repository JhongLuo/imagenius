export function useLatestNumNodes() {
  const latestNumNodes = ref()

  const uninitializedLnnVal = -1
  const lnnLabel = 'LNN'

  // initialize latestNumNodes from localStorage
  const storedLNN = localStorage.getItem(lnnLabel)
  latestNumNodes.value = storedLNN !== null ? Number(storedLNN) : uninitializedLnnVal

  watch(
    latestNumNodes,
    (newVal) => {
      localStorage.setItem(lnnLabel, newVal.toString())
    },
    { deep: true })

  return {
    latestNumNodes,
    uninitializedLnnVal,
  }
}
