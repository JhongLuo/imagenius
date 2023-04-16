<script setup lang="ts">
import type { Edges, Layouts, Nodes } from 'v-network-graph'
import { VNetworkGraph } from 'v-network-graph'
import * as vNG from 'v-network-graph'
// @ts-expect-error
import dagre from 'dagre/dist/dagre.min.js'
import TheLabeledInput from '~/components/TheInputs/TheLabeledInput.vue'

defineOptions({
  name: 'TreePage',
})

const api = useAPIStore()
const { toastsArray, blinkToast } = useToasts()

// graph style params
const nodeSize = 64
const edgeStrokeWidth = 2
const theNodes = ref<Nodes>({})
const theEdges = ref<Edges>({})
const layouts: Layouts = reactive({
  nodes: {},
})
const configs = vNG.defineConfigs({
  view: {
    scalingObjects: true,
  },
  node: {
    draggable: false,
    normal: {
      type: 'rect',
      width: nodeSize,
      height: nodeSize,
      borderRadius: 8,
      color: '#66b2b2',
    },
    hover: {
      color: '#66b2b2',
    },
    label: {
      visible: false,
    },
  },
  edge: {
    normal: {
      width: edgeStrokeWidth,
      color: '#66b2b2',
      linecap: 'round',
    },
    margin: 4,
    marker: {
      target: {
        type: 'arrow',
        width: 4,
        height: 4,
      },
    },
    hover: {
      color: '#66b2b2',
    },
  },
})
const graph = ref<vNG.Instance>()
const generateTreeLayout = () => {
  if (Object.keys(theNodes.value).length <= 1 || Object.keys(theEdges.value).length === 0)
    return

  // convert graph
  // ref: https://github.com/dagrejs/dagre/wiki
  const g = new dagre.graphlib.Graph()
  // Set an object for the graph label
  g.setGraph({
    rankdir: 'TB',
    nodesep: nodeSize * 2,
    edgesep: nodeSize,
    ranksep: nodeSize * 2,
  })
  // Default to assigning a new object as a label for each new edge.
  g.setDefaultEdgeLabel(() => ({}))

  // Add nodes to the graph. The first argument is the node id. The second is
  // metadata about the node. In this case we're going to add labels to each of
  // our nodes.
  Object.entries(theNodes.value).forEach(([nodeId, node]) => {
    g.setNode(nodeId, { label: node.name, width: nodeSize, height: nodeSize })
  })

  // Add edges to the graph.
  Object.values(theEdges.value).forEach((edge) => {
    g.setEdge(edge.source, edge.target)
  })

  dagre.layout(g)

  const box: Record<string, number | undefined> = {}
  g.nodes().forEach((nodeId: string) => {
    // update node position
    const x = g.node(nodeId).x
    const y = g.node(nodeId).y
    layouts.nodes[nodeId] = { x, y }

    // calculate bounding box size
    box.top = box.top ? Math.min(box.top, y) : y
    box.bottom = box.bottom ? Math.max(box.bottom, y) : y
    box.left = box.left ? Math.min(box.left, x) : x
    box.right = box.right ? Math.max(box.right, x) : x
  })

  const graphMargin = nodeSize * 2
  const viewBox = {
    top: (box.top ?? 0) - graphMargin,
    bottom: (box.bottom ?? 0) + graphMargin,
    left: (box.left ?? 0) - graphMargin,
    right: (box.right ?? 0) + graphMargin,
  }
  graph.value?.setViewBox(viewBox)
}

const imgKey = computed<string>(() => useRoute().query.key as string)
const imgKeyUserInput = ref<string>('')
const selectedPrompt = ref<string>('')
const isIniting = ref<boolean>(false)

const initTree = async () => {
  // start init
  isIniting.value = true
  try {
    const fd = new FormData()
    fd.append('key', imgKey.value)
    const response = await api.getTree(fd)
    utilsJS.validateResponse(response)
    // handle success
    const nodes = response.data.nodes
    const edges = response.data.edges
    Object.keys(nodes).forEach((key) => {
      theNodes.value[key] = nodes[key]
    })
    Object.keys(edges).forEach((key) => {
      theEdges.value[key] = edges[key]
    })
    // finish loading and start display
    await utils.sleep(50)
    isIniting.value = false
    generateTreeLayout()
    blinkToast(
      TOAST_ID__INIT_TREE__SUCCESS,
      'success',
      TOAST_MSG__INIT_TREE__SUCCESS)
  }
  catch (err) {
    // handle error
    blinkToast(
      TOAST_ID__INIT_TREE__ERROR,
      'error',
      err as string)
    isIniting.value = false
  }
}

onMounted(() => {
  if (imgKey.value !== undefined)
    initTree()
})

// const imgKey = computed<string>(() => useRoute().query.key as string)
</script>

<template>
  <!-- Page Title -->
  <h1
    my-title
  >
    Tree
  </h1>

  <div
    v-if="imgKey === undefined"
    w-md
    flex flex-row justify-between items-end
  >
    <div
      class="w-70%"
    >
      <TheLabeledInput
        input-id="input-tree-key"
        label-text="Image Key"
      >
        <TheIconedTextInput
          v-model.trim="imgKeyUserInput"
          icon="i-carbon:password"
          input-id="input-tree-key-str"
          placeholder="Key of img to search for..."
          @keydown.enter="utils.navigateToTree(imgKeyUserInput)"
        />
      </TheLabeledInput>
    </div>

    <!-- button: retrieve -->
    <TheButton
      label="Go"
      :disabled="imgKeyUserInput.length === 0"
      @click="utils.navigateToTree(imgKeyUserInput)"
    />
  </div>

  <!-- Page Content -->
  <div
    v-if="imgKey !== undefined"
    w-full h-full
  >
    <!-- floating prompt -->
    <div
      v-if="selectedPrompt !== ''"
      fixed bottom-5 left-5
      flex justify-center
    >
      <span
        px-3 py-1
        w-full h-min
        backdrop-blur-sm rounded-lg
        text-white select-none
        bg-truegray-7
      >
        {{ selectedPrompt }}
      </span>
    </div>

    <!-- center button -->
    <TheButton
      mb-4
      label="To Center"
      text-sm
      @click="graph?.panToCenter()"
    />

    <VNetworkGraph
      ref="graph"
      border border-rounded-xl border-gray-200 dark:border-gray-800
      w-2xl h-2xl mx-auto
      :nodes="theNodes"
      :edges="theEdges"
      :layouts="layouts"
      :configs="configs"
    >
      <!-- Replace the node component -->
      <template #override-node="{ nodeId, scale, config }">
        <image
          :x="-config.radius * scale * 2"
          :y="-config.radius * scale * 2"
          :width="config.radius * scale * 4"
          :height="config.radius * scale * 4"
          :xlink:href="theNodes[nodeId].src"
          cursor-pointer
          @click="utils.navigateToEdit(theNodes[nodeId].key)"
          @mouseover="selectedPrompt = theNodes[nodeId].prompt"
          @mouseleave="selectedPrompt = ''"
        />
      </template>
    </VNetworkGraph>
  </div>

  <!-- Toasts, Alerts & Modals -->
  <TheToasts
    :toasts-array="toastsArray"
  />
</template>
