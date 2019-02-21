#!/usr/bin/env python3


from ai.driver import AIDriver
from ai.heuristic import Heuristic
from tj_wriggle.decoder import Decoder
from util.args import Arguments
from util.timer import Timer
import os.path


# Constants
# Command line argument processing
DEFAULT_PUZZLE_PATH = 'puzzle1.txt'
DEFAULT_SOLN_PATH = 'solution1.txt'
DEFAULT_ARGUMENTS = [DEFAULT_PUZZLE_PATH, DEFAULT_SOLN_PATH]
DEFAULT_VALUES_STR = '  (1) Puzzle file path\n  (2) Solution file path'
    
# Heuristic to use
#  Heuristic.MANHATTAN_DIST: Smallest Manhattan distance between the wriggler's 
#    head/tail and the goal coordinate
#  Heuristic.NUM_OBSTACLES:  Number of obstacles between the wriggler's head/tail 
#    (whichever is closer to the goal) and the goal coordinate
HEURISTIC = Heuristic.NUM_OBSTACLES


if __name__ == '__main__':
    # Process command line arguments
    args = Arguments(len(DEFAULT_ARGUMENTS), DEFAULT_ARGUMENTS, DEFAULT_VALUES_STR)
    puzzle_path, soln_path = args.get_args()
    
    # Check to see if the puzzle path exists
    if not os.path.isfile(puzzle_path):
        # This path is invalid
        print('Invalid puzzle path \'%s\'' % puzzle_path)
            
        # Replace this puzzle path with a default puzzle path
        puzzle_path = DEFAULT_PUZZLE_PATH
        
    # Inform the user which puzzle is being solved
    print('Solving', puzzle_path + '...')

    # Decode puzzle
    puzzle_decoder = Decoder(puzzle_path)
    
    # Store decoded puzzle information
    initial_state = puzzle_decoder.get_initial_state()
    puzzle = puzzle_decoder.get_puzzle()
    
    # Create AI Driver
    ai_driver = AIDriver(initial_state, puzzle, HEURISTIC)
    
    # Execute tree search
    timer = Timer()
    timer.start()
    result = ai_driver.a_star_gs()
    elapsed_time = timer.end()
    
    # Check the result
    if result.solution:
        # A solution has been found
        print('\nSolution found.')
        print('N =', result.num_expanded_nodes)
        print('d =', result.max_depth)

        # Generate solution file
        puzzle.write_solution_file(soln_path, puzzle_path, result.solution.actions, result.solution.final_state, elapsed_time)
        
    else:
        print('\nCould not find a solution.\n')
