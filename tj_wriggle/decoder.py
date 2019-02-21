from tj_wriggle.chars import Chars
from tj_wriggle.coordinate import Coordinate
from tj_wriggle.directions import Directions
from tj_wriggle.puzzle import Puzzle
from tj_wriggle.state import State
from tj_wriggle.wriggler import Wriggler
import sys


class Decoder:
    def __init__(self, puzzle_path):
        """Initializes the Decoder class, which reads in and decodes 
        a given TJ-Wriggle puzzle.
        
        Where puzzle_path exists and is the path to the puzzle file to decode.
        """
        
        def can_conv_to_int(s):
            """Returns True if s can be converted to an int, False otherwise."""
            try: 
                int(s)
                return True

            except ValueError:
                return False


        def get_wrigglers():
            """Returns a list of wrigglers (Wriggler class instances) 
            found in self.puzzle.
            """
            
            def find_body_coords(coord, body_coords):
                """Recursively finds the body coordinates associated with given coordinate coord, 
                which could be a head coordinate or a body coordinate.
                """
                value_at_coord = self.puzzle[coord.x][coord.y]
                
                # Initialize new_coord in case of error
                new_coord = None
                
                if value_at_coord in [str(wriggler_index) for wriggler_index in range(self.num_wrigglers)]:
                    # The tail coordinate has been found
                    return

                elif value_at_coord == Chars.HEAD_UP.value    or \
                    value_at_coord == Chars.UP.value:
                    new_coord = Coordinate(coord.x - 1, coord.y)
                
                elif value_at_coord == Chars.HEAD_DOWN.value  or \
                    value_at_coord == Chars.DOWN.value:
                    new_coord = Coordinate(coord.x + 1, coord.y)
                    
                elif value_at_coord == Chars.HEAD_LEFT.value  or \
                    value_at_coord == Chars.LEFT.value:
                    new_coord = Coordinate(coord.x, coord.y - 1)

                elif value_at_coord == Chars.HEAD_RIGHT.value or \
                    value_at_coord == Chars.RIGHT.value:
                    new_coord = Coordinate(coord.x, coord.y + 1)

                body_coords.append(new_coord)
                return find_body_coords(new_coord, body_coords)
                

            tail_coords = set([])
            head_coords = set([])

            # Find all head and tail coordinates in the puzzle
            for x in range(self.height):
                for y in range(self.width):
                    if self.puzzle[x][y] in [str(wriggler_index) for wriggler_index in range(self.num_wrigglers)]:
                        # There is a tail at this coordinate
                        tail_coords.add(Coordinate(x, y))

                    elif self.puzzle[x][y] in [
                            Chars.HEAD_UP.value,
                            Chars.HEAD_DOWN.value,
                            Chars.HEAD_LEFT.value,
                            Chars.HEAD_RIGHT.value
                        ]:
                        # There is a head at this coordinate
                        head_coords.add(Coordinate(x, y))

            # Sanity check
            assert(len(tail_coords) == len(head_coords) == self.num_wrigglers)

            # Initialize wriggler list
            wrigglers = [None for _ in range(self.num_wrigglers)] 
            
            # From each head, find all segments that make up the body
            for head_coord in head_coords:
                body_coords = []
                find_body_coords(head_coord, body_coords)
                tail_coord = body_coords[-1]
                wriggler_index = int(self.puzzle[tail_coord.x][tail_coord.y])

                # Instantiate each wriggler with their body coordinates
                wrigglers[wriggler_index] = Wriggler([head_coord] + body_coords)
            
            return wrigglers


        # Read in puzzle file contents
        with open(puzzle_path, 'r') as puzzle_file:
            print(puzzle_path)
            self.puzzle = []

            try:
                # Attempt to read the puzzle file, checking for validity along the way
                height_count = 0
                for index, line in enumerate(puzzle_file):
                    if index == 0:
                        # The 0th line contains width, height, and the number of wrigglers
                        line_list = [line_item for line_item in line.split()]
                        
                        # There should be 3 items in this list
                        assert len(line_list) == 3
                        
                        for item in line_list:
                            # The items in this list should all convert nicely to ints
                            assert can_conv_to_int(item)

                        self.width, self.height, self.num_wrigglers = [int(line_item) for line_item in line_list]

                    else:
                        # Every subsequent line contains characters that make up the puzzle board
                        line_list = line.split()                        
                        
                        # This line should have self.width items
                        assert len(line_list) == self.width

                        self.puzzle.append(line_list)
                        
                        # We've seen another row, increment the height count
                        height_count += 1
                
                # The height count should be equal to the expected height
                assert height_count == self.height
            
            except AssertionError:
                print('Error: Puzzle file is not in the correct format.\n')
                sys.exit()

        # Store all wall coordinates and empty coordinates
        self.wall_coords = set([])
        self.empty_coords = set([])

        for x in range(self.height):
            for y in range(self.width):
                if self.puzzle[x][y] == Chars.WALL.value:
                    self.wall_coords.add(Coordinate(x, y))
                
                elif self.puzzle[x][y] == Chars.EMPTY.value:
                    self.empty_coords.add(Coordinate(x, y))
        
        self.wrigglers = get_wrigglers()

    
    def get_initial_state(self):
        """Returns the initial state of the TJ-Wriggle puzzle."""
        return State(self.wrigglers, self.empty_coords)
        
    
    def get_puzzle(self):
        """Returns the TJ-Wriggle puzzle data."""
        return Puzzle(self.width, self.height, self.num_wrigglers, self.wall_coords)
