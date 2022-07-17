#! /bin/bash
function run() {
    for i in $(seq 0 99); do
        seed=`printf "%04d\n" "${i}"`
        echo ${seed}
        `cargo run --release --bin tester python src2.py ${1} < in/${seed}.txt > out_search/${seed}.txt`
        # echo ${score}
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
    done < search_result.log
    echo ${score}
}

for area in $(seq 11 29);
do
    echo ${area}
    run ${area} >& search_result.log
    score | tee search_scores.log
done