#!/bin/bash

declare -a benchmarks=("blackscholes-sm" "fluidanimate-sm" "vips-sm")
declare -a schedulers=("bb" "ss")

logfile=quickia_log_`date +"%Y-%m-%d_%H%M"`.csv
rm -f $logfile

for b in "${benchmarks[@]}"
do
    for s in "${schedulers[@]}"
    do
        echo "INFO: Running benchmark $b with scheduler $s..."
        ./simulate_quickia.py --hp_tasks=$b --lp_tasks=$b --scheduler=$s --log=$logfile run
    done
done
