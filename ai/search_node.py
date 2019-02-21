class SearchNode:
    def __init__(self, state, parent_node=None, action=None, path_cost=1):
        """Initializes the SearchNode class."""
        self.state = state
        self.parent_node = parent_node
        self.action = action
        self.path_cost = path_cost


    def __hash__(self):
        return hash(self.state)


    def __eq__(self, other):
        return hash(self) == hash(other)
