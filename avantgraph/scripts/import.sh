
#!/bin/bash
set -e
DATA_DIR="../../../ldbc_snb_datagen_spark/out/graphs/json/bi/composite-projected-fk/initial_snapshot"
if [ -d "$DATA_DIR" ]; then
    echo "Merging JSON files in $DATA_DIR..."
    python3 merge-data.py "$DATA_DIR" ./data.json
else
    echo "Data directory $DATA_DIR does not exist."
    exit 1
fi
