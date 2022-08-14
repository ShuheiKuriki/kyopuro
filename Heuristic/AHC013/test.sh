#!/bin/bash
function run() {
    file=${1}
    seed=${2}
    `python ${file}.py < in/${seed}.txt > out_${file}/${seed}.txt`
}

function run_multi() {
    for i in $(seq 0 ${2}); do
        seed=`printf "%04d\n" "${i}"`
        echo ${seed}
        run ${1} ${seed}
    done
}

function score() {
    score=0
    file=${1}
    while read line
    do
        # echo $line
        if [[ "$line" =~ "Score = " ]]; then
            s=`echo ${line} | sed -r "s/Score = //"`
            score=$((score+s))
        fi
    done < result_${file}.log
    echo "${file} ${score}" | tee -a scores.log
}

function run_all() {
    file=${1}
    run_multi ${file} ${2} >& result_${file}.log
    score ${file}
}

if [ ${1} = "all" ];
then
    run_all first ${2}
    run_all src ${2}
else
    echo first
    run first ${1}
    echo src
    run src ${1}
fi