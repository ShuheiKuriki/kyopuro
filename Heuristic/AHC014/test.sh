#!/bin/bash
function run() {
    file=${1}
    seed=${2}
    `python ${file}.py < in/${seed}.txt > out_${file}/${seed}.txt`
}

function run_multi() {
    for i in $(seq 0 ${1}); do
        seed=`printf "%04d\n" "${i}"`
        echo ${seed}
        run "src" ${seed}
        echo 
    done
}

function score() {
    score=0
    file=${1}
    while read line
    do
        # echo $line
        if [[ "$line" =~ "score=" ]]; then
            s=`echo ${line} | sed -r "s/score=//"`
            score=$((score+s))
        fi
    done < result.log
    echo "${file} ${score}" | tee -a scores.log
}

if [ ${1} = "all" ];
then
    run_multi ${2} >& result.log
    score "src"
else
    run "src" ${1}
fi