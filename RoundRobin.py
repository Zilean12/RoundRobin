from collections import deque
from tabulate import tabulate

time_quantum = 2

class Process:
    def __init__(self, name, arrival_time, required_time):
        self.name = name
        self.arrival_time = arrival_time
        self.required_time = required_time
        self.time_processed = 0
        self.first_cpu_time = -1

    def __repr__(self):
        return self.name

p0 = Process('P1', 0, 5)
p1 = Process('P2', 1, 4)
p2 = Process('P3', 2, 2)
p3 = Process('P4', 4, 1)
processes = [p0, p1, p2, p3]
end_times = {process.name: 0 for process in processes}
wait_times = {process.name: 0 for process in processes}
response_times = {process.name: 0 for process in processes}
queue = deque()
running_proc = None  # Tracks running process in the CPU
running_proc_time = 0  # Tracks the time running process spent in the CPU

for t in range(12):
    # if any process arrived this time then append that to the queue
    if t == 0:
        for p in processes:
            if p.arrival_time == 0:
                queue.append(p)

    # if there are none processes then try to get a process from the queue
    if running_proc is None:
        if len(queue) > 0:
            running_proc = queue.popleft()
            if running_proc.first_cpu_time == -1:
                running_proc.first_cpu_time = t
            running_proc_time = 0
    
    # if any process is due to arrive in the next time then append that to the queue
    for p in processes:
        if p.arrival_time == t + 1:
            queue.append(p)
    
    # process the current process
    if running_proc is not None:
        running_proc.time_processed += 1
        running_proc_time += 1
        # if the current proces does not need any more execution
        if running_proc.required_time == running_proc.time_processed:
            end_times[str(running_proc)] = t + 1
            wait_times[str(running_proc)] = end_times[str(running_proc)] - running_proc.arrival_time - running_proc.required_time
            response_times[str(running_proc)] = running_proc.first_cpu_time - running_proc.arrival_time
            running_proc = None
            running_proc_time = 0
        # if the time_quatum allocated for this process exceeded then move the current process to the end of the queue
        elif running_proc_time >= time_quantum:
            queue.append(running_proc)
            running_proc = None
            running_proc_time = 0

print("----------------------------------------------------------------")
print("Running gantt Chart")
print(end_times)  # End times for each process

table = []
total_tat = 0
total_wt = 0
total_rt = 0
for p in processes:
    tat = end_times[p.name] - p.arrival_time
    wt = wait_times[p.name]
    rt = response_times[p.name]
    total_tat += tat
    total_wt += wt
    total_rt += rt
    table.append([p.name, p.arrival_time, p.required_time, end_times[p.name], tat, wt, rt])

print("")

print(tabulate(table, headers=["Process", "Arrival Time", "Burst Time", "Completion Time", "Turnaround Time", "Waiting Time", "Response Time"], tablefmt="grid"))
print("")

print("----------------------------------------------------------------")
print(f"Average Turnaround Time: {total_tat / len(processes):.2f}")
print(f"Average Waiting Time: {total_wt / len(processes):.2f}")
print(f"Average Response Time: {total_rt / len(processes):.2f}")
print("----------------------------------------------------------------")

