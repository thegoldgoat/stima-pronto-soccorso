import heapq


class MyPriorityQueue:
    '''
        Not using queue.PriorityQueue since it has thread safety (not needed)
        and cannot easily create a deep clone.
    '''

    # Create a heap with the array given (**must** be heapified)
    def __init__(self, heap=None, bool_heapify=False):
        if heap is None:
            self.heap = []
        else:
            self.heap = heap
            if bool_heapify == True:
                heapq.heapify(self.heap)

    def push(self, new_item):
        heapq.heappush(self.heap, new_item)

    def pop(self):
        return heapq.heappop(self.heap)

    def get_min(self):
        return self.heap[0]

    def is_empty(self):
        return len(self.heap) == 0
