#!/usr/bin/env python3


from ai.driver import AIDriver
from ai.heuristic import Heuristic
from tj_wriggle.decoder import Decoder
from util.args import Arguments
from util.timer import Timer
import numpy
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
HEURISTIC = Heuristic.MANHATTAN_DIST


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
            
        # Calculate the effective branching factor b_star
        # b_star^(d + 1) - (N + 1)*b_star + N = 0
        N = result.num_expanded_nodes
        d = result.max_depth
        
        # Construct the coefficient list in accordance with the above equation
        coefficients = [N, -1 * N - 1]

        # Set coefficients from b_star^2 to b_star^(d + 1) to 0
        coefficients += [0] * d

        # Reset coefficient of b_star^(d + 1) to 1
        coefficients[-1] = 1

        # Reverse the coefficient list to the order that numpy expects
        coefficients = coefficients[::-1]
        
        # Generate the solutions
        solution_list = numpy.roots(coefficients)

        # Only take real valued solutions
        solution_list = [numpy.real(solution) for solution in solution_list[numpy.isreal(solution_list)]]

        # Find the valid solution
        solution = None
        for possible_solution in solution_list:
            if possible_solution > 1:
                solution = possible_solution
                break
        
        if solution:
            print('b* = %.5f' % solution)

        else:
            print('b* could not be found')
        
        # Generate solution file
        puzzle.write_solution_file(soln_path, puzzle_path, result.solution.actions, result.solution.final_state, elapsed_time)
        
    else:
        print('\nCould not find a solution.\n')
