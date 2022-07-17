#! /bin/bash
function run() {
    seed=${1}
    `cargo run --release --bin tester python src.py < in/${seed}.txt > out/${seed}.txt`
}

function run_multi() {
    for i in $(seq 0 ${1}); do
        seed=`printf "%04d\n" "${i}"`
        echo ${seed}
        run ${seed}
    done
}

function score() {
    score=0
    while read line
    do
        if [[ "$line" =~ "Score = " ]]; then
            # echo ${line#Score = }
            score=$((score+${line#Score = }))
        fi
    done < result.log
    echo ${score} | tee -a scores.log
}

if [ ${1} = "all" ];
then
    run_multi ${2} >& result.log
    score
else
    run ${1}
fi