import time


class Timer:
    def __init__(self):
        """Initializes the Timer class, which calculates 
        wall time in seconds.
        """
        self.start_time = None
        self.end_time = None
        self.elapsed_time = None
    
    
    def start(self):
        """Starts the timer."""
        self.start_time = time.time()
    
    
    def end(self):
        """Ends the timer and returns elapsed time.
        
        This function requires that the start function
        has already been called.
        """
        self.end_time = time.time()
        
        if not self.start_time:
            # The start function was never called
            return None

        self.elapsed_time = self.end_time - self.start_time
        return self.elapsed_time
    
    
    def reset(self):
        self.start_time = None
        self.end_time = None
        self.elapsed_time = None
