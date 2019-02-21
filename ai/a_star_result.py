from ai.generic_result import GenericResult


class AStarResult(GenericResult):
    def __init__(self, solution=None, failure=False, num_expanded_nodes=0, max_depth=0):
        """Initializes the AStarResult class, which encapsulates results
        from the A*GS algorithm. This includes the number of expanded nodes 
        and the max depth reached by the algorithm, which are used in 
        calculating the effective branching factor.
        """
        self.solution = solution
        self.failure = failure
        self.num_expanded_nodes = num_expanded_nodes
        self.max_depth = max_depth
