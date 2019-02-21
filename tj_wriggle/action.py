from tj_wriggle.end import WrigglerEnd


class Action:
    def __init__(self, move_to_coord, wriggler_index, wriggler_end):
        """Initializes the Action class."""
        self.move_to_coord = move_to_coord
        self.wriggler_index = wriggler_index
        self.wriggler_end = wriggler_end
    
    
    def __str__(self):
        """Returns a string representation of the action."""
        end_str = 'head' if self.wriggler_end == WrigglerEnd.HEAD else 'tail'

        return 'Move ' + str(self.wriggler_index) + '\'s ' + end_str + \
            ' to coordinate ' + str(self.move_to_coord)
