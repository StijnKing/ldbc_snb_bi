#!/bin/bash
set -e 

# Set default container image if not provided
export PLATFORM_VERSION="2.12_spark3.2"
export DATAGEN_VERSION="0.5.1+23-1d60a657"
export LDBC_SNB_DATAGEN_JAR="/home/stijn/git/ldbc_snb_datagen_spark/target/ldbc_snb_datagen_2.12_spark3.2-0.5.1+23-1d60a657-jar-with-dependencies.jar"
export SPARK_HOME="${HOME}/spark-3.2.2-bin-hadoop3.2"
export PATH="${SPARK_HOME}/bin":"${PATH}"

# # Navigate CWD to the script's directory
for scale_factor in "0.003" "0.1" "0.3" "1" "3"
do
    echo "Processing scale factor: $scale_factor"

    cd ../../ldbc_snb_datagen_spark

    # Generate the graph data using the specified configuration
    rm -rf out/graphs
    ./tools/run.py -- --format json --scale-factor $scale_factor --mode bi --explode-attrs --explode-edges

    cd -  # Return to the original directory

    # Iterate over the different configurations to generate data sets
    for config in "1 0.01 0.01" "5 0.05 0.05" "10 0.25 0.1" "20 0.5 0.2"
    do
        read -r max_size node_frac type_frac <<< "$config"
        echo "Measuring load time for config: max_size=${max_size}, node_frac=${node_frac}, type_frac=${type_frac}"

        export NODE_REIFICATION_CHANCE="${node_frac}"
        export POPULATOR_AMOUNT="${max_size}"
        export POPULATOR_CHANCE="${type_frac}"

        # Suffix output with the config parameters to create different data sets
        python3 ./scripts/merge-data.py ../../ldbc_snb_datagen_spark/out/graphs/json/bi/singular-projected-fk/initial_snapshot ./data/snb-bi-SF${scale_factor}-${max_size}-${node_frac}-${type_frac}.json
    done
done
