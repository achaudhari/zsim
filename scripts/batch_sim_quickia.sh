#!/bin/bash

declare -a benchmarks=("blackscholes-sm" "fluidanimate-sm" "raytrace" "swaptions-sm" "vips-sm" "x264-sm")
declare -a schedulers=("auto" "fair")

filename=data_singles_`date +"%Y-%m-%d_%H%M"`
rm -f ${filename}.csv
rm -f ${filename}.log

for s in "${schedulers[@]}"
do
    for b in "${benchmarks[@]}"
    do
        echo "==============================================================="
        echo "Running benchmark $b with scheduler $s"
        echo "==============================================================="
        ./simulate_quickia.py --hp_tasks=$b --scheduler=$s --log=${filename}.csv run | tee -a ${filename}.log
    done
done
