#!/bin/bash
set -e 

# Set default container image if not provided
AG_IMAGE=${AG_IMAGE:-stijnking/avantgraph-mpg:latest}
OUTPUT_FILE_NAME="scalefactor_query_times.csv"

echo "Using AvantGraph image: ${AG_IMAGE}"
# Setup headers for CSV output
echo "scale_factor,max_size,node_fraction,type_fraction,query_number,run_time_seconds,iteration" > ./data/${OUTPUT_FILE_NAME}
# Represents (scale_factor, max_size, node_fraction, type_fraction)
for scale_factor in "0.003" "0.1" "0.3" "1"
do
    echo "Processing scale factor: $scale_factor"
    for config in "1 0.01 0.01" "5 0.05 0.05" "10 0.25 0.1" "20 0.5 0.2"
    do
        read -r max_size node_frac type_frac <<< "$config"
        echo "Measuring load time for config: max_size=${max_size}, node_frac=${node_frac}, type_frac=${type_frac}"

        FILEPATH="/data/snb-bi-SF${scale_factor}-${max_size}-${node_frac}-${type_frac}.json"

        docker run -it --rm -v ./data:/data -v ./scripts:/scripts --cap-add SYS_ADMIN --cap-add SYS_PTRACE --privileged ${AG_IMAGE} /scripts/create-schema.sh
        docker run -it --rm -v ./data:/data -v ./scripts:/scripts --cap-add SYS_ADMIN --cap-add SYS_PTRACE --privileged -e DATA_FILE="${FILEPATH}" ${AG_IMAGE} /scripts/load-graph.sh

        # Run all 11 queries for this configuration in total 20 times
        for query_num in {1..11}
        do
            query_name="mpg-${query_num}.cypher"
            echo "Running query: ${query_name}"

            for i in {1..20}
            do
                echo "  Iteration: ${i}"

                # Run the benchmark and measure the loading time
                START_TIME=$(date +%s)
                docker run -it --rm -v ./data:/data -v ./scripts:/scripts -v ./queries:/queries --cap-add SYS_ADMIN --cap-add SYS_PTRACE -p 7687:7687 --privileged -e DATA_FILE="${FILEPATH}" ${AG_IMAGE} avantgraph --query-type=cypher --enable-mpg /data/snb-bi /queries/${query_name}
                END_TIME=$(date +%s)

                RUN_TIME=$((END_TIME - START_TIME))
                echo "Query time for config (scale_factor=${scale_factor}, max_size=${max_size}, node_frac=${node_frac}, type_frac=${type_frac}, query=${query_num}, iteration=${i}): ${RUN_TIME} seconds"
                echo "${scale_factor},${max_size},${node_frac},${type_frac},${query_num},${RUN_TIME},${i}" >> ./data/${OUTPUT_FILE_NAME}
            done
        done
    done
done
