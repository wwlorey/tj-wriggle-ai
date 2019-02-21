from tj_wriggle.action import Action
from tj_wriggle.chars import Chars
from tj_wriggle.coordinate import Coordinate
from tj_wriggle.directions import Directions
from tj_wriggle.end import WrigglerEnd
from tj_wriggle.state import State
from tj_wriggle.wriggler import Wriggler


class Puzzle:
    def __init__(self, width, height, num_wrigglers, wall_coords):
        """Initializes the TJ-Wriggle Puzzle class."""
        self.width = width
        self.height = height
        self.num_wrigglers = num_wrigglers
        self.wall_coords = wall_coords
        self.goal_coord = Coordinate(self.height - 1, self.width - 1)
        
    
    def get_actions(self, state):
        """Returns the available actions applicable to the given
        state.
        """
        actions = []

        # Iterate through all wrigglers in the state
        for wriggler_index, wriggler in enumerate(state.wriggler_list):
            # Get possible coordinates the wriggler can move from
            move_from_coords = [wriggler.get_head(), wriggler.get_tail()] 
            
            # Generate possible actions for both ends of the wriggler
            for wriggler_end, move_from_coord in enumerate(move_from_coords):
                # Get valid, empty, adjacent coordinates that can be moved to from
                #  the move_from_coord                
                adj_coords = self.get_adj_coords(state, move_from_coord)

                # Add the possible actions that can be made to the actions list
                for move_to_coord in adj_coords:
                    actions.append(Action(move_to_coord, wriggler_index, \
                        WrigglerEnd.HEAD if WrigglerEnd.HEAD.value == wriggler_end else WrigglerEnd.TAIL))
        
        return actions
    
    
    def get_result(self, state, action):
        """Returns the resulting state obtained after applying the
        given action to the given state.
        """
        # Copy state contents into new variables
        new_wriggler_list = []
        new_empty_coords = set([])

        for wriggler in state.wriggler_list:
            new_wriggler_list.append(Wriggler([Coordinate(body_coord.x, body_coord.y) for body_coord in wriggler.body_coords]))
        
        for empty_coord in state.empty_coords:
            new_empty_coords.add(Coordinate(empty_coord.x, empty_coord.y))

        # Adjust the empty coordinates to account for the move
        new_empty_coords.remove(action.move_to_coord)
        
        if action.wriggler_end == WrigglerEnd.HEAD:
            # The coordinate previously occupied by the tail is now empty
            # Reflect this in the empty coordinate list
            new_empty_coords.add(new_wriggler_list[action.wriggler_index].get_tail())
            
            # Adjust this wriggler's body coordinates
            new_wriggler_list[action.wriggler_index].body_coords = [action.move_to_coord] + new_wriggler_list[action.wriggler_index].body_coords[:-1]
        
        else: # action.wriggler_end == WrigglerEnd.TAIL
            # The coordinate previously occupied by the head is now empty
            # Reflect this in the empty coordinate list
            new_empty_coords.add(new_wriggler_list[action.wriggler_index].get_head())

            # Adjust this wriggler's body coordinates
            new_wriggler_list[action.wriggler_index].body_coords = new_wriggler_list[action.wriggler_index].body_coords[1:] + [action.move_to_coord]
        
        return State(new_wriggler_list, new_empty_coords)
    

    def check_goal_state(self, state):
        """Returns True if the given state is the goal state,
        False otherwise.
        
        A goal state is represented by the 0th wriggler (the blue wriggler) 
        occupying the bottom-right puzzle corner with either its head or tail.
        """
        return state.wriggler_list[0].get_head() == self.goal_coord or \
               state.wriggler_list[0].get_tail() == self.goal_coord
        
    
    def get_adj_coords(self, state, coord):
        """Returns a list of valid, empty coordinates adjacent to the
        given coordinate c for the given state.
        """
        valid_adj_coords = []

        # Add coordinates that are valid to valid_adj_coords
        if not coord.x == 0:
            valid_adj_coords.append(Coordinate(coord.x - 1, coord.y))

        if not coord.x == self.height - 1:
            valid_adj_coords.append(Coordinate(coord.x + 1, coord.y))
        
        if not coord.y == 0:
            valid_adj_coords.append(Coordinate(coord.x, coord.y - 1))
        
        if not coord.y == self.width - 1:
            valid_adj_coords.append(Coordinate(coord.x, coord.y + 1))
        
        # Return coordinates from valid_adj_coords that are empty
        return [coord for coord in valid_adj_coords if coord in state.empty_coords]
    
    
    def visualize(self, state):
        """Returns a string representing a visualization of the puzzle 
        with given state applied to it.
        """
        # Initialize a 2D array of empty characters
        # An array is used so that it can be altered, it will be converted
        #  to a string at the end of the function
        puzzle = [[Chars.EMPTY.value for _ in range(self.width)] for _ in range(self.height)]
        
        # Insert walls
        for c in self.wall_coords:
            puzzle[c.x][c.y] = Chars.WALL.value
        
        # Insert wrigglers
        for wriggler_index, wriggler in enumerate(state.wriggler_list):
            tail_coord  = wriggler.get_tail()
            
            # Set the wriggler's index on the puzzle grid
            puzzle[tail_coord.x][tail_coord.y] = str(wriggler_index)
            
            # Insert wriggler body characters
            for body_index in range(len(wriggler.body_coords) - 1):
                this_body_segment = wriggler.body_coords[body_index]
                next_body_segment = wriggler.body_coords[body_index + 1]
                
                # Find the direction of the next body segment
                if this_body_segment.x > next_body_segment.x and this_body_segment.y == next_body_segment.y:
                    next_segment_direction = Directions.UP

                elif this_body_segment.x < next_body_segment.x and this_body_segment.y == next_body_segment.y:
                    next_segment_direction = Directions.DOWN

                elif this_body_segment.x == next_body_segment.x and this_body_segment.y > next_body_segment.y:
                    next_segment_direction = Directions.LEFT

                else: # this_body_segment.x == next_body_segment.x and this_body_segment.y < next_body_segment.y
                    next_segment_direction = Directions.RIGHT
                
                # Find the appropriate character to insert corresponding to the direction of the next segment
                if body_index == 0:
                    # This is a head segment
                    if next_segment_direction == Directions.UP:
                        value = Chars.HEAD_UP.value                    

                    elif next_segment_direction == Directions.DOWN:
                        value = Chars.HEAD_DOWN.value                    

                    elif next_segment_direction == Directions.RIGHT:
                        value = Chars.HEAD_RIGHT.value                    

                    else: # next_segment_direction == Directions.LEFT
                        value = Chars.HEAD_LEFT.value                    
                
                else:
                    # This is a body segment
                    if next_segment_direction == Directions.UP:
                        value = Chars.UP.value 

                    elif next_segment_direction == Directions.DOWN:
                        value = Chars.DOWN.value 

                    elif next_segment_direction == Directions.RIGHT:
                        value = Chars.RIGHT.value 

                    else: # next_segment_direction == Directions.LEFT
                        value = Chars.LEFT.value 
                
                puzzle[this_body_segment.x][this_body_segment.y] = value
        
        # From left to right: return a string separated by 
        #  newline characters that is made up of space separated
        #  characters for each line in the puzzle
        return '\n'.join([' '.join(line) for line in puzzle])


    def write_solution_file(self, soln_path, puzzle_path, actions, final_state, wall_time):
        """Writes the solution file."""
        soln_str = ''

        for action in actions:
            soln_str += str(action.wriggler_index) + ' '
            soln_str += ('0' if action.wriggler_end == WrigglerEnd.HEAD else '1') + ' '
            soln_str += str(action.move_to_coord.y) + ' '
            soln_str += str(action.move_to_coord.x) + '\n'
        
        soln_str += self.visualize(final_state) + '\n'
        soln_str += str(wall_time) + '\n'  
        soln_str += str(len(actions))
        
        # Write to file
        with open(soln_path, 'w') as f:
            f.write(soln_str)
            
        print('Solution written to ' + soln_path + '\n')
        