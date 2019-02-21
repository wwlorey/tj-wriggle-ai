class State:
    def __init__(self, wriggler_list, empty_coords):
        """Initializes the TJ-Wriggle State class."""
        self.wriggler_list = wriggler_list
        self.empty_coords = empty_coords

    def __hash__(self):
        return int(''.join([str(hash(wriggler)) for wriggler in self.wriggler_list]))
            
        
    def __eq__(self, other):
        return hash(self) == hash(other)

    
    def __contains__(self, coord):
        """Returns True if the given coordinate contains a Wriggler body segment. 
        False otherwise.
        """
        for wriggler in self.wriggler_list:
            if coord in wriggler:
                return True
        
        return False
