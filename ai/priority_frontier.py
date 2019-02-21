from heapq import heappush, heappop
import itertools


class PriorityFrontier():
    def __init__(self):
        """Initializes the PriorityFrontier (priority queue) class."""
        # A heap queue of [heuristic, count, node] lists
        self.queue = []
        
        # Counter used for assigning a count to each node
        self.counter = itertools.count()

        # Nodes that are currently in the queue
        # Both the key & value are the node for fast lookup & retrival
        self.node_dict = {}

        # Nodes that have been removed from the queue
        self.removed_nodes = set()


    def __contains__(self, node):
        return node in self.node_dict


    def peek_node(self, node):
        """Returns the node equal to the given node from the nodes list.
        
        This function assumes that the given node is in the nodes list.
        """
        return self.node_dict[node][-1]
        

    def peek_heuristic(self, node):
        """Returns the heuristic from the node equal to the given node from the nodes list.
        
        This function assumes that the given node is in the nodes list.
        """
        return self.node_dict[node][0]
        

    def is_empty(self):
        """Returns True if the frontier is empty, False otherwise."""
        return len(self.queue) == 0
    

    def insert(self, node, heuristic):
        """Adds the given node to the frontier."""
        count = next(self.counter)
        entry = [heuristic, count, node]
        self.node_dict[node] = entry
        heappush(self.queue, entry)


    def remove_node(self, node):
        """Removes the node equal to the given node from the queue."""
        entry = self.node_dict.pop(node)
        self.removed_nodes.add(entry[-1])


    def pop(self):
        """Removes & returns the element with the lowest heuristic value
        from the frontier.
        """
        while self.queue:
            heuristic, count, node = heappop(self.queue)

            if node is not self.removed_nodes:
                return node
        
        return None
