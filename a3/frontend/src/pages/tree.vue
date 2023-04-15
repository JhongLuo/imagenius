<script setup lang="ts">
import { VNetworkGraph } from "v-network-graph"
import "v-network-graph/lib/style.css"

import { reactive } from "vue"
import * as vNG from "v-network-graph"
import { Nodes, Edges } from "v-network-graph"
import {
  ForceLayout,
  ForceNodeDatum,
  ForceEdgeDatum
} from "v-network-graph/lib/force-layout"


const nodes: Nodes = {
  node1: { name: "N1" },
  node2: { name: "N2" },
  node3: { name: "N3" },
  node4: { name: "N4" },
  node5: { name: "N5" },
  node6: { name: "N6" },
  node7: { name: "N7" },
}

const edges: Edges = {
  edge1: { source: "node1", target: "node2" },
  edge2: { source: "node2", target: "node3" },
  edge3: { source: "node3", target: "node4" },
  edge4: { source: "node3", target: "node5" },
  edge5: { source: "node2", target: "node6" },
  edge6: { source: "node6", target: "node7" },
}

const configs = reactive(
  vNG.defineConfigs({
    view: {
      layoutHandler: new ForceLayout({
        positionFixedByDrag: false,
        positionFixedByClickWithAltKey: true,
        // * The following are the default parameters for the simulation.
        createSimulation: (d3, nodes, edges) => {
          const forceLink = d3.forceLink<ForceNodeDatum, ForceEdgeDatum>(edges).id(d => d.id)
          return d3
            .forceSimulation(nodes)
            .force("edge", forceLink.distance(50))
            .force("charge", d3.forceManyBody())
            .force("collide", d3.forceCollide(50).strength(0.2))
            .force("center", d3.forceCenter().strength(0.05))
            .alphaMin(0.001)
        }
      }),
    },
    node: {
      label: {
        visible: false,
      },
    },
    edge: {
    marker: {
      target: {
        type: "arrow",
        width: 4,
        height: 4,
      },
    },
  },
  })
)


</script>

<template>
<ThePageContent>
    <v-network-graph
        :zoom-level="0.5"
        :nodes="nodes"
        :edges="edges"
        :configs="configs"
    />
</ThePageContent>
</template>
