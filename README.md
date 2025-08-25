

---

# CPU Scheduling Simulator

This project is a Python-based simulator for different **CPU scheduling algorithms** from Operating Systems.
It lets you enter process details and see how algorithms like **FCFS, SJF, Round Robin, and Priority Scheduling** work in action.
The program also generates a **Gantt Chart** so you can visualize the CPU execution order.

---

## Features

* First Come First Serve (FCFS)
* Shortest Job First (SJF) – Preemptive & Non-Preemptive
* Round Robin (with time quantum)
* Priority Scheduling
* Gantt Chart visualization with different colors
* Calculates Completion Time, Turnaround Time, and Waiting Time

---

## Example Output

```
Process | AT | BT | CT | TAT | WT
     P1 |  0 |  7 | 12 |  12 |  5
     P2 |  2 |  4 |  7 |   5 |  1
     P3 |  4 |  1 |  5 |   1 |  0

Average TAT = 6.00
Average WT = 2.00
```

---

## How to Run

1. Clone the repository:

   ```bash
   git clone https://github.com/bhavanabc05/cpu-scheduling-simulator.git
   cd cpu-scheduling-simulator
   ```
2. Install matplotlib (for charts):

   ```bash
   pip install matplotlib
   ```
3. Run the script:

   ```bash
   python cpu_scheduling.py
   ```

---

## Tech Stack

* Python 3
* Matplotlib (for visualization)

---

## Why I Built This

I created this project to strengthen my understanding of **CPU scheduling algorithms** and to get hands-on practice in **Python and data visualization**. It helped me clearly see the differences in waiting times and turnaround times between algorithms.

---


