#!/bin/bash

set -e

# Default location of the data file inside the container but allow override
DATA_FILE=${DATA_FILE:-/data/snb-bi.json}
GRAPH_FILE=${GRAPH_FILE:-/data/snb-bi}

# Load graph
ag-load-graph "${DATA_FILE}" "${GRAPH_FILE}" --graph-format=json --load-properties --load-reification-data
