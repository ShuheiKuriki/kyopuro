#! /bin/bash
function run() {
    seed=${1}
    echo -n "${seed} " >> std_err.log
    echo ${seed} >> info.log
    ./tester.exe python src.py < in/${seed}.txt > out/${seed}.txt 2>> std_err.log
    # ./vis.exe in/${seed}.txt out/${seed}.txt
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
        # if [[ "$line" =~ "W, K, C = " ]]; then
        #     WKC=${line#W, K, C = }
        #     echo "${WKC}" >> result.csv
        # fi
        if [[ "$line" =~ .*Total\ Cost\ =\ .* ]]; then
            # echo ${line#Total Cost = }
            score=${line#*Total Cost = }
            echo "${score}" >> result.csv
            total_score=$((total_score+score))
            seed=$((seed+1))
        fi
    done < std_err.log
    echo "total_score = ${total_score}" | tee -a scores.log
}

# echo "" > result.log
echo "" > std_err.log
echo "" > info.log
if [ ${1} = "all" ];
then
    testcase=${2}
    run_multi ${testcase}
    score
else
    seed=${1}
    run ${seed}
fi