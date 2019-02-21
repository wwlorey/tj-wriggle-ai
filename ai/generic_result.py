class GenericResult:
    def __init__(self, solution=None, failure=False):
        """Initializes the GenericResult class, which encapsulates results
        from search algorithms requiring 'generic' search output in ai.driver
        """
        self.solution = solution
        self.failure = failure
