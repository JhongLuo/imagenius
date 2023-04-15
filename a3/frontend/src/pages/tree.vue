<script setup lang="ts">
import { VNetworkGraph, Nodes, Edges, EventHandlers } from "v-network-graph"
import "v-network-graph/lib/style.css"
import { reactive } from "vue"
import * as vNG from "v-network-graph"
import {
  ForceLayout,
  ForceNodeDatum,
  ForceEdgeDatum
} from "v-network-graph/lib/force-layout"



const nodes: Nodes = {
  node1: { name: "This is...", src: "https://s3.amazonaws.com/ece1779t18a3cache/1", prompt: "This is the whole prompt"},
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
        // The following are the default parameters for the layout simulation.
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
            visible: true,
        },
        normal: {
            type: "circle",
            radius: 32,
            color: "#4466cc",
        },
        hover: {
            radius: 64,
        },
    },
    edge: {
        margin: 2,
        normal: {
            width: 4,
            color: "#4466cc",
            dasharray: "0",
            linecap: "round",

        },
        marker: {
            target: {
                type: "angle",
            },
        },

  },
  })
)

const eventHandlers: EventHandlers = {
  "node:click": ({ node }) => {
    // redirect to node's editing page
    console.log(node)
    console.log(nodes[node].src)
  },
  "node:pointerover": ({ node }) => {
    // show prompt
    console.log(nodes[node].prompt)
  },
  "node:pointerout": _ => {
    // hide prompt
  },
}


</script>

<template>
<ThePageContent>
    <div
        class="mt-8 grid gap-4"
        style="width: 80%; height: 500px;"
    >
        <v-network-graph
            :zoom-level="1"
            :nodes="nodes"
            :edges="edges"
            :configs="configs"
            :event-handlers="eventHandlers"
        >
            <defs>
                <!--
                    Define the path for clipping the image.
                    To change the size of the applied node as it changes,
                    add the `clipPathUnits="objectBoundingBox"` attribute
                    and specify the relative size (0.0~1.0).
                -->
                <clipPath id="aiCircle" clipPathUnits="objectBoundingBox">
                    <circle cx="0.5" cy="0.5" r="0.5" />
                </clipPath>
            </defs>

                <!-- Replace the node component -->
            <template #override-node="{ nodeId, scale, config, ...slotProps }">
                <!-- circle for filling background -->
                <circle
                    class="ai-circle"
                    :r="config.radius * scale"
                    fill="#ffffff"
                    v-bind="slotProps"
                />
                <!--
                    The base position of the <image /> is top left. The node's
                    center should be (0,0), so slide it by specifying x and y.
                -->
                <image
                    class="ai-picture"
                    :x="-config.radius * scale"
                    :y="-config.radius * scale"
                    :width="config.radius * scale * 2"
                    :height="config.radius * scale * 2"
                    :href="`${nodes[nodeId].src}`"
                    clip-path="url(#aiCircle)"
                />
                <!-- circle for drawing stroke -->
                <circle
                    class="ai-circle"
                    :r="config.radius * scale"
                    fill="none"
                    stroke="#808080"
                    :stroke-width="1 * scale"
                    v-bind="slotProps"
                />
            </template>
        </v-network-graph>
        <div
            
        >
        </div>    
    </div>
</ThePageContent>
</template>

<style lang="scss" scoped>
    // transitions when scaling on mouseover.
    .ai-circle,
    .ai-picture {
    transition: all 0.1s linear;
    }

    // suppress image events so that mouse events are received
    // by the background circle.
    .ai-picture {
    pointer-events: none;
    }
</style>