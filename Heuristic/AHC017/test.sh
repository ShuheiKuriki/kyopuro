#! /bin/bash
function run() {
    seed=${1}
    echo ${seed} >> result.log
    python src.py < in/${seed}.txt > out/${seed}.txt 2>> result.log
    ./vis.exe in/${seed}.txt out/${seed}.txt
}

function run_multi() {
    testcase=${1}
    for i in $(seq 0 ${testcase}); do
        seed=`printf "%04d\n" "${i}"`
        # echo ${seed}
        run ${seed}
    done
}

function score() {
    total_score=0
    seed=0
    echo "" > result.csv
    while read line
    do
        if [[ "$line" =~ "Score = " ]]; then
            # echo ${line#Score = }
            score=${line#Score = }
            echo "${score}" >> result.csv
            total_score=$((total_score+score))
            seed=$((seed+1))
        fi
    done < scores.log
    echo "total_score = ${total_score}" | tee -a scores.log
}

echo "" > result.log
if [ ${1} = "all" ];
then
    testcase=${2}
    run_multi ${testcase} >& scores.log
    score
else
    seed=${1}
    run ${seed}
fi