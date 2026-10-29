"""
Data Structures for CPU Scheduling Mini Project.
Implements:
1. Queue (First-In, First-Out)
2. PriorityQueue (Min-Heap: smaller priority number = higher priority)
"""

import heapq

class Queue:
    """Standard First-In-First-Out (FIFO) Queue."""
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        """Add item to rear of queue."""
        self.items.append(item)

    def dequeue(self):
        """Remove and return front item."""
        if self.is_empty():
            return None
        return self.items.pop(0)

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

    def to_list(self):
        return list(self.items)


class PriorityQueue:
    """Priority Queue where lowest priority number gets highest priority."""
    def __init__(self):
        self.heap = []
        self._counter = 0  # Tie-breaker for stable ordering

    def push(self, item, priority):
        """Insert item with priority key."""
        heapq.heappush(self.heap, (priority, self._counter, item))
        self._counter += 1

    def pop(self):
        """Remove and return item with highest priority (lowest number)."""
        if self.is_empty():
            return None
        priority, _, item = heapq.heappop(self.heap)
        return item

    def is_empty(self):
        return len(self.heap) == 0

    def size(self):
        return len(self.heap)

    def to_list(self):
        """Return items sorted by priority without mutating the heap."""
        sorted_heap = sorted(self.heap, key=lambda x: (x[0], x[1]))
        return [item for _, _, item in sorted_heap]
