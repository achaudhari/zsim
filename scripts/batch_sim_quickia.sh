#!/bin/bash

declare -a benchmarks=("blackscholes-lg" "x264-lg")
declare -a schedulers=("1b" "1s" "bb" "ss" "bs")

logfile=quickia_log_`date +"%Y-%m-%d_%H%M"`.csv
rm -f $logfile

for s in "${schedulers[@]}"
do
    for b in "${benchmarks[@]}"
    do
        echo "INFO: Running benchmark $b with scheduler $s..."
        ./simulate_quickia.py --hp_tasks=$b --scheduler=$s --log=$logfile run
    done
done
