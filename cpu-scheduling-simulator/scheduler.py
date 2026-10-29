"""
CPU Scheduler implementations using Queue and Priority Queue.
Calculates Completion Time (CT), Turnaround Time (TAT), and Waiting Time (WT).
"""

from dsa import Queue, PriorityQueue

PALETTE = ["#3b82f6", "#10b981", "#f59e0b", "#ec4899", "#8b5cf6", "#06b6d4"]

class Process:
    def __init__(self, pid, arrival_time, burst_time, priority=1, color=None):
        self.pid = str(pid)
        self.arrival_time = int(arrival_time)
        self.burst_time = int(burst_time)
        self.priority = int(priority)
        self.color = color

        # Result metrics
        self.start_time = None
        self.completion_time = None
        self.turnaround_time = 0
        self.waiting_time = 0

    def to_dict(self):
        return {
            "pid": self.pid,
            "arrival_time": self.arrival_time,
            "burst_time": self.burst_time,
            "priority": self.priority,
            "color": self.color,
            "start_time": self.start_time,
            "completion_time": self.completion_time,
            "turnaround_time": self.turnaround_time,
            "waiting_time": self.waiting_time
        }


def prepare_processes(raw_procs):
    procs = []
    for i, p in enumerate(raw_procs):
        color = p.get("color") or PALETTE[i % len(PALETTE)]
        procs.append(Process(
            pid=p.get("pid", f"P{i+1}"),
            arrival_time=int(p.get("arrival_time", 0)),
            burst_time=int(p.get("burst_time", 1)),
            priority=int(p.get("priority", 1)),
            color=color
        ))
    return procs


def run_queue_scheduling(raw_procs):
    """
    Queue Scheduling (FIFO / FCFS):
    Arriving processes are enqueued to the rear of the Queue.
    The CPU dequeues and runs the front process to completion.
    """
    procs = prepare_processes(raw_procs)
    queue = Queue()
    unvisited = sorted(procs, key=lambda p: (p.arrival_time, p.pid))
    
    time = 0
    completed = []
    gantt_chart = []
    dsa_states = []  # Snapshots of queue at key decision points

    while len(completed) < len(procs):
        # 1. Enqueue newly arrived processes
        arrived = [p for p in unvisited if p.arrival_time <= time and p not in queue.to_list() and p not in completed]
        for p in arrived:
            queue.enqueue(p)

        if queue.is_empty():
            # CPU is IDLE until next arrival
            next_proc = min([p for p in unvisited if p not in completed], key=lambda p: p.arrival_time)
            idle_duration = next_proc.arrival_time - time
            gantt_chart.append({
                "pid": "IDLE",
                "start": time,
                "end": next_proc.arrival_time,
                "duration": idle_duration,
                "color": "#334155"
            })
            time = next_proc.arrival_time
            continue

        # 2. Dequeue process from front of queue
        curr = queue.dequeue()
        curr.start_time = time
        curr.completion_time = time + curr.burst_time
        curr.turnaround_time = curr.completion_time - curr.arrival_time
        curr.waiting_time = curr.turnaround_time - curr.burst_time

        gantt_chart.append({
            "pid": curr.pid,
            "start": time,
            "end": curr.completion_time,
            "duration": curr.burst_time,
            "color": curr.color
        })

        time = curr.completion_time
        completed.append(curr)

        # Snapshot queue after execution
        dsa_states.append({
            "time": time,
            "dispatched": curr.pid,
            "queue": [p.pid for p in queue.to_list()]
        })

    return calculate_metrics("Queue (FIFO)", "Queue", completed, gantt_chart, dsa_states)


def run_priority_queue_scheduling(raw_procs):
    """
    Priority Queue Scheduling:
    Arriving processes are pushed into the Priority Queue (Min-Heap).
    The CPU pops and executes the process with the highest priority (lowest number).
    """
    procs = prepare_processes(raw_procs)
    pq = PriorityQueue()
    unvisited = sorted(procs, key=lambda p: (p.arrival_time, p.pid))
    
    time = 0
    completed = []
    gantt_chart = []
    dsa_states = []

    while len(completed) < len(procs):
        # 1. Push arrived processes into PriorityQueue
        arrived = [p for p in unvisited if p.arrival_time <= time and p not in pq.to_list() and p not in completed]
        for p in arrived:
            pq.push(p, p.priority)

        if pq.is_empty():
            next_proc = min([p for p in unvisited if p not in completed], key=lambda p: p.arrival_time)
            idle_duration = next_proc.arrival_time - time
            gantt_chart.append({
                "pid": "IDLE",
                "start": time,
                "end": next_proc.arrival_time,
                "duration": idle_duration,
                "color": "#334155"
            })
            time = next_proc.arrival_time
            continue

        # 2. Pop process with highest priority (smallest number)
        curr = pq.pop()
        curr.start_time = time
        curr.completion_time = time + curr.burst_time
        curr.turnaround_time = curr.completion_time - curr.arrival_time
        curr.waiting_time = curr.turnaround_time - curr.burst_time

        gantt_chart.append({
            "pid": curr.pid,
            "start": time,
            "end": curr.completion_time,
            "duration": curr.burst_time,
            "color": curr.color
        })

        time = curr.completion_time
        completed.append(curr)

        dsa_states.append({
            "time": time,
            "dispatched": curr.pid,
            "queue": [p.pid for p in pq.to_list()]
        })

    return calculate_metrics("Priority Queue (Min-Heap)", "Priority Queue", completed, gantt_chart, dsa_states)


def calculate_metrics(title, dsa_type, completed_procs, gantt_chart, dsa_states):
    n = len(completed_procs)
    avg_tat = round(sum(p.turnaround_time for p in completed_procs) / n, 2) if n > 0 else 0
    avg_wt = round(sum(p.waiting_time for p in completed_procs) / n, 2) if n > 0 else 0

    # Sort results by PID or completion
    completed_procs.sort(key=lambda p: (p.arrival_time, p.pid))

    return {
        "title": title,
        "dsa_type": dsa_type,
        "processes": [p.to_dict() for p in completed_procs],
        "gantt_chart": gantt_chart,
        "dsa_states": dsa_states,
        "avg_tat": avg_tat,
        "avg_wt": avg_wt,
        "total_time": gantt_chart[-1]["end"] if gantt_chart else 0
    }
