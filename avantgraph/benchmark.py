from datetime import datetime
from dateutil.relativedelta import relativedelta
import time
import os
import csv
import datetime
import neo4j
from queries import run_queries, run_precomputations
from pathlib import Path
from itertools import cycle
import argparse


if __name__ == '__main__':
    query_variants = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]

    driver = neo4j.GraphDatabase.driver("bolt://localhost:7687")
    session = driver.session()

    parser = argparse.ArgumentParser()
    parser.add_argument('--scale_factor', type=str, help='Scale factor', required=True)
    parser.add_argument('--test', action='store_true', help='Test execution: 1 query/batch', required=False)
    parser.add_argument('--pgtuning', action='store_true', help='Paramgen tuning execution: 100 queries/batch', required=False)
    args = parser.parse_args()
    sf = args.scale_factor
    test = args.test
    pgtuning = args.pgtuning

    output = Path(f'output/output-sf{sf}')
    output.mkdir(parents=True, exist_ok=True)
    open(f"output/output-sf{sf}/results.csv", "w").close()
    open(f"output/output-sf{sf}/timings.csv", "w").close()

    results_file = open(f"output/output-sf{sf}/results.csv", "a")
    timings_file = open(f"output/output-sf{sf}/timings.csv", "a")
    timings_file.write(f"tool|sf|day|batch_type|q|parameters|time\n")

    network_start_date = datetime.date(2012, 11, 29)
    network_end_date = datetime.date(2013, 1, 1)
    test_end_date = datetime.date(2012, 12, 2)
    batch_size = relativedelta(days=1)
    batch_date = network_start_date

    benchmark_start = time.time()

    batch_type = "power"
    run_precomputations(sf, query_variants, session, batch_date, batch_type, timings_file)
    reads_time = run_queries(query_variants, session, sf, batch_date, batch_type, test, pgtuning, timings_file, results_file)

    benchmark_end = time.time()
    benchmark_duration = benchmark_end - benchmark_start
    benchmark_file = open(f"output/output-sf{sf}/benchmark.csv", "w")
    benchmark_file.write(f"time\n")
    benchmark_file.write(f"{benchmark_duration:.6f}\n")
    benchmark_file.close()

    results_file.close()
    timings_file.close()
