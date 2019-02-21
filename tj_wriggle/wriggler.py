class Wriggler:
    def __init__(self, body_coords):
        """Initializes the Wriggler class."""
        self.body_coords = body_coords
        
    
    def __hash__(self):
        return int(''.join([str(coord.x) + str(coord.y) + str(index) for index, coord in enumerate(self.body_coords)]))
        

    def __eq__(self, other):
        return hash(self) == hash(other)
        
        
    def __contains__(self, coord):
        return coord in self.body_coords

    
    def get_head(self):
        """Returns the head coordinate of this wriggler."""
        return self.body_coords[0]
    
    
    def get_tail(self):
        """Returns the tail coordinate of this wriggler."""
        return self.body_coords[-1]
