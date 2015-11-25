#!/bin/bash

declare -a benchmarks
declare -a schedulers=("auto" "fair")

# Generate all unique pairs of benchmarks from the list
set -- "blackscholes-sm" "fluidanimate-sm" "raytrace" "swaptions-sm" "vips-sm" "x264-sm"
for a; do
    shift
    for b; do
        benchmarks=("${benchmarks[@]}" "$a,$b")
    done
done

logfile=data_pairs_`date +"%Y-%m-%d_%H%M"`.csv
rm -f $logfile

for s in "${schedulers[@]}"
do
    for b in "${benchmarks[@]}"
    do
        echo "==============================================================="
        echo "Running benchmark $b with scheduler $s"
        echo "==============================================================="
        ./simulate_quickia.py --hp_tasks=$b --scheduler=$s --log=$logfile run
    done
done
