class DLSResult:
    def __init__(self, solution=None, cutoff=False, failure=False):
        """Initializes the DLSResult class, which encapsulates results
        from the dls function in ai.driver
        """
        self.solution = solution
        self.cutoff = cutoff
        self.failure = failure
