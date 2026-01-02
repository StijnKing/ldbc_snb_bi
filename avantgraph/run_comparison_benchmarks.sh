#!/bin/bash
set -e 

# Set default container image if not provided
AG_IMAGE=${AG_IMAGE:-stijnking/avantgraph-mpg:latest}
OUTPUT_FILE_NAME="comparison_query_times.csv"

echo "Using AvantGraph image: ${AG_IMAGE}"

# Clear output files if they exist
> ./data/${OUTPUT_FILE_NAME}

# Setup headers for CSV output
echo "with_mpg,query_number,run_time_milliseconds,iteration" > ./data/${OUTPUT_FILE_NAME}

for with_mpg in true false
do
    FILEPATH="/data/snb-bi.json"

    # docker run -it --rm -v ./data:/data -v ./scripts:/scripts --cap-add SYS_ADMIN --cap-add SYS_PTRACE --privileged ${AG_IMAGE} /scripts/create-schema-without-reification.sh
    # docker run -it --rm -v ./data:/data -v ./scripts:/scripts --cap-add SYS_ADMIN --cap-add SYS_PTRACE --privileged -e DATA_FILE="${FILEPATH}" ${AG_IMAGE} /scripts/load-graph-without-reification.sh

    # Run all 11 queries for this configuration in total 20 times
    for query_num in {1..5}
    do
        if [ "$with_mpg" = true ] ; then
            query_name="pg-${query_num}-clean.cypher"
        else
            query_name="pg-${query_num}-raw.cypher"
        fi
        echo "Running query: ${query_name}"

        for i in {1..10}
        do
            echo "  Iteration: ${i}"

            # Run the benchmark and measure the loading time
            START_TIME=$(date +%s%3N)
            docker run -it --rm -v ./data:/data -v ./scripts:/scripts -v ./queries:/queries --cap-add SYS_ADMIN --cap-add SYS_PTRACE -p 7687:7687 --privileged -e DATA_FILE="${FILEPATH}" ${AG_IMAGE} avantgraph --query-type=cypher --enable-mpg /data/snb-bi /queries/${query_name}
            END_TIME=$(date +%s%3N)

            RUN_TIME=$((END_TIME - START_TIME))
            echo "Query time for config (scale_factor=${scale_factor}, max_size=${max_size}, node_frac=${node_frac}, type_frac=${type_frac}, query=${query_num}, iteration=${i}): ${RUN_TIME} milliseconds"
            echo "${with_mpg},${query_num},${RUN_TIME},${i}" >> ./data/${OUTPUT_FILE_NAME}
        done
    done
done
