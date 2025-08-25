import matplotlib.pyplot as plt
import matplotlib.cm as cm

# ---------- Utility Functions ----------
def print_results(processes):
    print("\nProcess | AT | BT | CT | TAT | WT")
    for p in processes:
        print(f"{p['pid']:>7} | {p['arrival']:>2} | {p['burst']:>2} | {p['ct']:>2} | {p['tat']:>3} | {p['wt']:>2}")
    avg_tat = sum(p['tat'] for p in processes) / len(processes)
    avg_wt = sum(p['wt'] for p in processes) / len(processes)
    print(f"\nAverage TAT = {avg_tat:.2f}")
    print(f"Average WT = {avg_wt:.2f}")


def draw_gantt_chart(gantt, title="Gantt Chart"):
    fig, gnt = plt.subplots()
    gnt.set_xlabel("Time")
    gnt.set_ylabel("Processes")
    gnt.set_title(title)

    processes = [p[0] for p in gantt if p[0] != 'Idle']
    unique_processes = list(dict.fromkeys(processes))

    cmap = cm.get_cmap('tab20', len(unique_processes))
    color_map = {proc: cmap(i) for i, proc in enumerate(unique_processes)}
    color_map['Idle'] = 'lightgray'

    for i, (p, start, end) in enumerate(gantt):
        gnt.broken_barh(
            [(start, end - start)],
            (10, 9),
            facecolors=color_map[p],
            edgecolor="black"
        )
        gnt.text((start + end) / 2, 14, p, ha='center', va='center', color='black')

    handles = [plt.Rectangle((0,0),1,1, color=color_map[p]) for p in unique_processes + ['Idle']]
    gnt.legend(handles, unique_processes + ['Idle'], title="Processes", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.show()


# ---------- Scheduling Algorithms ----------
def fcfs(processes):
    processes = sorted(processes, key=lambda x: x['arrival'])
    time, gantt = 0, []

    for p in processes:
        if time < p['arrival']:
            gantt.append(("Idle", time, p['arrival']))
            time = p['arrival']
        start = time
        time += p['burst']
        p['ct'] = time
        p['tat'] = p['ct'] - p['arrival']
        p['wt'] = p['tat'] - p['burst']
        gantt.append((p['pid'], start, time))
    return processes, gantt


def sjf_non_preemptive(processes):
    n = len(processes)
    processes = sorted(processes, key=lambda x: (x['arrival'], x['burst']))
    completed, time, gantt = 0, 0, []

    while completed < n:
        ready = [p for p in processes if 'ct' not in p and p['arrival'] <= time]
        if not ready:
            gantt.append(("Idle", time, time + 1))
            time += 1
            continue
        p = min(ready, key=lambda x: x['burst'])
        start = time
        time += p['burst']
        p['ct'] = time
        p['tat'] = p['ct'] - p['arrival']
        p['wt'] = p['tat'] - p['burst']
        gantt.append((p['pid'], start, time))
        completed += 1
    return processes, gantt


def sjf_preemptive(processes):
    n = len(processes)
    procs = [{**p, "remaining": p['burst']} for p in processes]
    time, completed, gantt = 0, 0, []

    while completed < n:
        ready = [p for p in procs if p['arrival'] <= time and p['remaining'] > 0]
        if not ready:
            gantt.append(("Idle", time, time + 1))
            time += 1
            continue
        p = min(ready, key=lambda x: x['remaining'])
        start = time
        time += 1
        p['remaining'] -= 1
        gantt.append((p['pid'], start, time))
        if p['remaining'] == 0:
            p['ct'] = time
            p['tat'] = p['ct'] - p['arrival']
            p['wt'] = p['tat'] - p['burst']
            completed += 1

    # Merge consecutive slots for clarity
    merged = []
    for pid, s, e in gantt:
        if merged and merged[-1][0] == pid:
            merged[-1] = (pid, merged[-1][1], e)
        else:
            merged.append((pid, s, e))

    return procs, merged


def priority_scheduling(processes):
    n = len(processes)
    for p in processes:
        p['priority'] = int(input(f"Enter Priority for {p['pid']} (lower = higher priority): "))

    time, completed, gantt = 0, 0, []
    while completed < n:
        ready = [p for p in processes if 'ct' not in p and p['arrival'] <= time]
        if not ready:
            gantt.append(("Idle", time, time + 1))
            time += 1
            continue
        p = min(ready, key=lambda x: (x['priority'], x['arrival']))
        start = time
        time += p['burst']
        p['ct'] = time
        p['tat'] = p['ct'] - p['arrival']
        p['wt'] = p['tat'] - p['burst']
        gantt.append((p['pid'], start, time))
        completed += 1
    return processes, gantt


def round_robin(processes, quantum):
    procs = [{**p, "remaining": p['burst']} for p in processes]
    time, gantt = 0, []
    queue = [p for p in sorted(procs, key=lambda x: x['arrival'])]
    completed = 0

    while completed < len(procs):
        if not queue:
            gantt.append(("Idle", time, time + 1))
            time += 1
            queue = [p for p in procs if p['remaining'] > 0 and p['arrival'] <= time]
            continue

        p = queue.pop(0)
        if p['arrival'] > time:
            gantt.append(("Idle", time, p['arrival']))
            time = p['arrival']

        start = time
        exec_time = min(quantum, p['remaining'])
        time += exec_time
        p['remaining'] -= exec_time
        gantt.append((p['pid'], start, time))

        if p['remaining'] == 0:
            p['ct'] = time
            p['tat'] = p['ct'] - p['arrival']
            p['wt'] = p['tat'] - p['burst']
            completed += 1
        else:
            queue.extend([q for q in procs if q['arrival'] <= time and q['remaining'] > 0 and q not in queue])
            queue.append(p)
    return procs, gantt


# ---------- Main ----------
if __name__ == "__main__":
    n = int(input("Enter number of processes: "))
    processes = []
    for i in range(n):
        pid = f"P{i+1}"
        arrival = int(input(f"Enter Arrival Time for {pid}: "))
        burst = int(input(f"Enter Burst Time for {pid}: "))
        processes.append({"pid": pid, "arrival": arrival, "burst": burst})

    print("\nChoose Scheduling Algorithm:")
    print("1. FCFS")
    print("2. SJF (Non-preemptive)")
    print("3. SJF (Preemptive - SRTF)")
    print("4. Priority Scheduling")
    print("5. Round Robin")
    choice = int(input("Enter choice: "))

    if choice == 1:
        result, gantt = fcfs(processes)
        print_results(result)
        draw_gantt_chart(gantt, "FCFS Scheduling - Gantt Chart")

    elif choice == 2:
        result, gantt = sjf_non_preemptive(processes)
        print_results(result)
        draw_gantt_chart(gantt, "SJF (Non-preemptive) Scheduling - Gantt Chart")

    elif choice == 3:
        result, gantt = sjf_preemptive(processes)
        print_results(result)
        draw_gantt_chart(gantt, "SJF (Preemptive - SRTF) Scheduling - Gantt Chart")

    elif choice == 4:
        result, gantt = priority_scheduling(processes)
        print_results(result)
        draw_gantt_chart(gantt, "Priority Scheduling - Gantt Chart")

    elif choice == 5:
        quantum = int(input("Enter Time Quantum: "))
        result, gantt = round_robin(processes, quantum)
        print_results(result)
        draw_gantt_chart(gantt, "Round Robin Scheduling - Gantt Chart")

    else:
        print("Invalid choice!")
