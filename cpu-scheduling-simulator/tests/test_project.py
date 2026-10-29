"""
Unit tests for Queue, Priority Queue, and Scheduling logic.
"""

import unittest
from dsa import Queue, PriorityQueue
from scheduler import run_queue_scheduling, run_priority_queue_scheduling
from app import app

class TestMiniProject(unittest.TestCase):
    def setUp(self):
        self.procs = [
            {"pid": "P1", "arrival_time": 0, "burst_time": 4, "priority": 3},
            {"pid": "P2", "arrival_time": 1, "burst_time": 3, "priority": 1},
            {"pid": "P3", "arrival_time": 2, "burst_time": 1, "priority": 4},
            {"pid": "P4", "arrival_time": 3, "burst_time": 2, "priority": 2}
        ]

    def test_queue_fifo(self):
        q = Queue()
        self.assertTrue(q.is_empty())
        q.enqueue("A")
        q.enqueue("B")
        self.assertEqual(q.dequeue(), "A")
        self.assertEqual(q.dequeue(), "B")
        self.assertTrue(q.is_empty())

    def test_priority_queue(self):
        pq = PriorityQueue()
        self.assertTrue(pq.is_empty())
        pq.push("Task Low", priority=5)
        pq.push("Task High", priority=1)
        pq.push("Task Med", priority=3)
        self.assertEqual(pq.pop(), "Task High")
        self.assertEqual(pq.pop(), "Task Med")
        self.assertEqual(pq.pop(), "Task Low")
        self.assertTrue(pq.is_empty())

    def test_queue_scheduler(self):
        res = run_queue_scheduling(self.procs)
        self.assertEqual(res["dsa_type"], "Queue")
        self.assertEqual(len(res["processes"]), 4)
        self.assertGreater(res["avg_tat"], 0)
        self.assertGreater(res["avg_wt"], 0)

    def test_priority_queue_scheduler(self):
        res = run_priority_queue_scheduling(self.procs)
        self.assertEqual(res["dsa_type"], "Priority Queue")
        self.assertEqual(len(res["processes"]), 4)
        # In priority queue, P2 (priority 1) should be scheduled before P4 or P3
        gantt_pids = [b["pid"] for b in res["gantt_chart"] if b["pid"] != "IDLE"]
        self.assertEqual(gantt_pids[0], "P1")  # arrived at 0
        self.assertEqual(gantt_pids[1], "P2")  # priority 1

    def test_flask_endpoints(self):
        client = app.test_client()
        res = client.get("/")
        self.assertEqual(res.status_code, 200)

        res = client.post("/api/simulate", json={"mode": "queue", "processes": self.procs})
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["dsa_type"], "Queue")

        res = client.post("/api/simulate", json={"mode": "priority_queue", "processes": self.procs})
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["dsa_type"], "Priority Queue")

if __name__ == "__main__":
    unittest.main()
