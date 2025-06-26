#!/usr/bin/env bash

docker exec --tty ${AG_CONTAINER_NAME} /workspaces/avantgraph/build/src/tools/server/ag-server --listen 0.0.0.0:listen /workspaces/avantgraph/data/snb-bi
