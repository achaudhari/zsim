#!/bin/bash

declare -a benchmarks=("blackscholes-sm" "fluidanimate-sm" "facesim-sm" "swaptions-sm" "x264-sm" "vips-sm" "raytrace" "bodytrack-sm" "freqmine-sm")
declare -a schedulers=("1b" "1s" "bb" "ss" "bs" "fair")

logfile=quickia_log_`date +"%Y-%m-%d_%H%M"`.csv
rm -f $logfile

for b in "${benchmarks[@]}"
do
    for s in "${schedulers[@]}"
    do
        echo "INFO: Running benchmark $b with scheduler $s..."
        ./simulate_quickia.py --hp_tasks=$b --scheduler=$s --log=$logfile --instr_window=10000000-210000000 run
    done
done
