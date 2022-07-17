# assign random tasks to team member 1.
import sys
import random
# Prior information
N, M, K, R = list(map(int, input().split()))
task_difficulty = []
for _ in range(N): task_difficulty.append(list(map(int, input().split())))
task_dependency = [[] for _ in range(N)]
for i in range(R):
    u, v = list(map(int, input().split()))
    task_dependency[v-1].append(u-1)
# -1: not started
#  0: started
#  1: completed
task_status = [-1] * N
# -1: not assigned
#  k: assigned task k (0 <= k <= N-1)
member_status = [-1] * M
day = 0
while True:
    day += 1
    output = []
    for member in range(M):
        # random search for tasks
        if member_status[member] < 0:
            tasklist = list(range(N))
            # random.shuffle(tasklist)
            for task in tasklist:
                if task_status[task] != -1: continue
                ready = True
                for necessary in task_dependency[task]:
                    if task_status[necessary] != 1:
                        # the dependent tasks have not been completed
                        ready = False
                        break
                if ready:
                    # assign the task to team member 1
                    task_status[task] = 0
                    member_status[member] = task
                    output.append(member+1)
                    output.append(task+1)
                    break
    print(len(output) // 2, *output)
    # After the output, you have to flush Standard Output
    sys.stdout.flush()
    n, *F = list(map(int, input().split()))
    if n == -1:
        # elapsed days == 2000, or all the tasks have been completed
        exit()
    elif n == 0:
        # no change in state
        pass
    else:
        for member in F:
            member -= 1
            finished_task = member_status[member]
            task_status[finished_task] = 1
            member_status[member] = -1