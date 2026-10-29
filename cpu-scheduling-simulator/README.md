# CPU Scheduling Mini Project: Queue & Priority Queue
> **College Mini Project in Operating Systems & Data Structures (DSA)**  
> Built with **Python (Flask)** and **Tailwind CSS**.

---

## 📌 Project Overview
This mini project demonstrates the two primary data structures used in Operating System CPU scheduling:
1. **Queue (FIFO / First-Come, First-Served)**: Arriving processes are appended to the rear; the CPU always dequeues and executes the process at the front.
2. **Priority Queue (Min-Heap)**: Arriving processes are inserted with a priority rating; the CPU always pops and executes the process with the highest priority (lowest priority number).

---

## 🚀 Data Structures Implemented

### 1. `Queue` (`dsa.py`)
- **`enqueue(item)`**: Inserts a process at the rear ($O(1)$).
- **`dequeue()`**: Removes and returns the process from the front ($O(1)$).
- **`is_empty()`**: Checks if any processes are waiting.

### 2. `PriorityQueue` (`dsa.py`)
- **`push(item, priority)`**: Inserts a process into the binary min-heap ($O(\log n)$).
- **`pop()`**: Extracts the process with the minimum priority key ($O(\log n)$).
- **`is_empty()`**: Checks if the heap is empty.

---

## 📐 Formulas & Performance Metrics

- **Turnaround Time (TAT)**: $\text{TAT} = \text{Completion Time (CT)} - \text{Arrival Time (AT)}$
- **Waiting Time (WT)**: $\text{WT} = \text{Turnaround Time (TAT)} - \text{Burst Time (BT)}$
- **Average Turnaround Time**: $\frac{\sum \text{TAT}}{N}$
- **Average Waiting Time**: $\frac{\sum \text{WT}}{N}$

---

## 🖥️ How to Run the Project

1. Run the launcher:
   ```bash
   python run.py
   ```
2. Your browser will automatically open:
   `http://127.0.0.1:5000`

3. Run automated tests:
   ```bash
   python -m unittest discover -s tests -v
   ```

---

## 📂 Project Structure

```
cpu-scheduling-simulator/
├── app.py              # Flask Web Server & REST API
├── run.py              # One-click launcher script
├── dsa.py              # Pure Queue & Priority Queue data structures
├── scheduler.py        # Queue & Priority Queue scheduling engines
├── templates/
│   └── index.html      # Minimalistic, modern single-page dashboard
├── tests/
│   └── test_project.py # Automated unit tests
├── requirements.txt    # Flask>=3.0.0
└── README.md           # Documentation & Viva notes
```
