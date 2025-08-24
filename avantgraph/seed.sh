python3 ./scripts/merge-data.py ../../ldbc_snb_datagen_spark/out/graphs/json/bi/singular-projected-fk/initial_snapshot ./data/snb-bi.json

# Set default container image if not provided
AG_IMAGE=${AG_IMAGE:-stijnking/avantgraph-mpg:latest}

docker run -it --rm -v ./data:/data -v ./scripts:/scripts --cap-add SYS_ADMIN --cap-add SYS_PTRACE --privileged ${AG_IMAGE} /scripts/create-graph-schema.sh
