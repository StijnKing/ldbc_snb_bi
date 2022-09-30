#!/bin/bash

set -eu
set -o pipefail

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd ..

. scripts/vars.sh

if [ ! -d "${TG_PARAMETER}" ]; then
    echo "Parameter directory ${TG_PARAMETER} does not exist."
    exit 1
fi

python3 -u queries.py --para ${TG_PARAMETER} --endpoint ${TG_ENDPOINT} --scale_factor ${SF} $@
