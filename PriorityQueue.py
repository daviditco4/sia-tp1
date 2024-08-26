import heapq  # Importing the heapq module for heap queue operations
import itertools  # Importing the itertools module for creating iterators


class PriorityQueue:
    def __init__(self):
        self.heap = []  # Initialize an empty list to store the heap
        self.entry_finder = {}  # Initialize a dictionary to map items to their heap entries
        self.REMOVED = '<removed-item>'  # Placeholder for a removed item
        self.counter = itertools.count()  # Unique sequence count to ensure the order of items with the same priority

    def add_item(self, item, priority=0, tiebreak=0):
        if item in self.entry_finder:
            self.remove_item(item)  # Remove the existing item if it is already in the queue
        count = next(self.counter)  # Get the next unique sequence count
        entry = [priority, tiebreak, count, item]  # Create a new entry with priority, tiebreak, count, and item
        self.entry_finder[item] = entry  # Add the entry to the entry_finder dictionary
        heapq.heappush(self.heap, entry)  # Push the entry onto the heap

    def remove_item(self, item):
        entry = self.entry_finder.pop(item)  # Remove the entry from the entry_finder dictionary
        entry[-1] = self.REMOVED  # Mark the entry as removed

    def pop_item(self):
        while self.heap:
            priority, _, _, item = heapq.heappop(self.heap)  # Pop the entry with the lowest priority from the heap
            if item is not self.REMOVED:
                del self.entry_finder[item]  # Remove the item from the entry_finder dictionary
                return priority, item  # Return the priority and item
        raise KeyError('Pop from an empty priority queue')  # Raise an error if the heap is empty

    def is_empty(self):
        return not self.entry_finder  # Return True if the entry_finder dictionary is empty, otherwise False