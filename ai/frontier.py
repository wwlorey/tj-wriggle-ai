class Frontier:
    def __init__(self):
        """Initializes the Frontier (FIFO queue) class."""
        self.nodes = []

    
    def is_empty(self):
        """Returns True if the frontier is empty, False otherwise."""
        return len(self.nodes) == 0
    
    
    def pop(self):
        """Removes & returns the element at the 0th position
        of the frontier.
        """
        return self.nodes.pop(0)
    
    
    def insert(self, node):
        """Appends the given node to the frontier."""
        self.nodes.append(node)
