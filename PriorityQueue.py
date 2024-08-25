import heapq
import itertools


class PriorityQueue:
    def __init__(self):
        self.heap = []
        self.entry_finder = {}
        self.REMOVED = '<removed-item>'
        self.counter = itertools.count()

    def add_item(self, item, priority=0, tiebreak=0):
        if item in self.entry_finder:
            self.remove_item(item)
        count = next(self.counter)
        entry = [priority, tiebreak, count, item]
        self.entry_finder[item] = entry
        heapq.heappush(self.heap, entry)

    def remove_item(self, item):
        entry = self.entry_finder.pop(item)
        entry[-1] = self.REMOVED

    def pop_item(self):
        while self.heap:
            priority, _, _, item = heapq.heappop(self.heap)
            if item is not self.REMOVED:
                del self.entry_finder[item]
                return priority, item
        raise KeyError('Pop from an empty priority queue')

    def is_empty(self):
        return not self.entry_finder
