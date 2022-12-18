#! /bin/bash
function run() {
    eps=${1}
    seed=${2}
    `./tester.exe python src.py < eps_${eps}/in/${seed}.txt > eps_${eps}/out/${seed}.txt` 2>> eps_${eps}/result.log
}

function run_multi() {
    testcase=${1}
    eps=${2}
    for i in $(seq 0 ${testcase}); do
        seed=`printf "%04d\n" "${i}"`
        echo ${seed}
        run ${eps} ${seed}
    done
}

function score() {
    score=0
    E=0
    while read line
    do
        if [[ "$line" =~ "Score = " ]]; then
            # echo ${line#Score = }
            score=$((score+${line#Score = }))
        fi
        if [[ "$line" =~ "E = " ]]; then
            # echo ${line#Score = }
            E=$((E+${line#E = }))
        fi
    done < eps_${eps}/result.log
    echo "score=${score} totalE=${E}" | tee -a eps_${eps}/scores.log
}

if [ ${1} = "all" ];
then
    testcase=${2}
    eps=${3}
    run_multi ${testcase} ${eps} >& eps_${eps}/result.log
    score ${eps}
else
    seed=${1}
    eps=${2}
    run ${eps} ${seed}
fi