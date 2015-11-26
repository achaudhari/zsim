#!/bin/bash

script_arg1=$1

declare -a benchmarks=("blackscholes-sm" "fluidanimate-sm" "raytrace" "swaptions-sm" "vips-sm" "x264-sm")
declare -a schedulers=("auto" "fair")

filename=data_singles_`date +"%Y-%m-%d_%H%M"`_`git rev-parse --verify HEAD --short`
rm -f ${filename}.csv
rm -f ${filename}.log

trap "echo Aborted by user!; exit;" SIGINT SIGTERM

for s in "${schedulers[@]}"
do
    for b in "${benchmarks[@]}"
    do
        echo "==============================================================="
        echo "Running benchmark $b with scheduler $s"
        echo "==============================================================="
        if [[ $script_arg1 = "--test" ]]; then
            ./simulate_quickia.py --hp_tasks=$b --scheduler=$s --instr_window=100000-200000 run | grep "DEBUG:"
        else        
            ./simulate_quickia.py --hp_tasks=$b --scheduler=$s --log=${filename}.csv run | tee -a ${filename}.log
        fi    
    done
done
