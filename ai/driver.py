from ai.a_star_result import AStarResult
from ai.dls_result import DLSResult
from ai.frontier import Frontier
from ai.generic_result import GenericResult
from ai.heuristic import Heuristic
from ai.priority_frontier import PriorityFrontier
from ai.search_node import SearchNode
from ai.solution import Solution
from itertools import count
from tj_wriggle.coordinate import Coordinate


class AIDriver:
    def __init__(self, initial_state, puzzle, heuristic=Heuristic.MANHATTAN_DIST):
        """Initializes the AIDriver Class, which encapsulates
        the solving of a given puzzle.
        """
        self.initial_state = initial_state
        self.get_actions = puzzle.get_actions
        self.get_result = puzzle.get_result
        self.check_goal_state = puzzle.check_goal_state
        self.goal_coord = puzzle.goal_coord
        self.wall_coords = puzzle.wall_coords
        self.heuristic = heuristic
    

    def bfts(self):
        """Performs a Breadth-First Tree Search (BFTS) on the puzzle's search space starting 
        at the initial state.
        
        Returns a GenericResult class instance containing a solution with final state and a 
        list of actions signifying the path from initial state to goal state if a solution 
        can be found. If a solution cannot be found, a GenericResult class instance indicating 
        a search failure is returned.
        """
        print('Performing BFTS\n')

        frontier = Frontier()
        frontier.insert(SearchNode(self.initial_state))
        
        while True:
            if frontier.is_empty():
                # Search failure
                return GenericResult(failure=True)
            
            # Get the next leaf node from the frontier
            leaf_node = frontier.pop()
            
            # Check for the goal state
            if self.check_goal_state(leaf_node.state):
                # Search success
                # Return final state and list of actions along path to the goal
                #  as part of the GenericResult class solution member
                return GenericResult(solution=Solution(final_state=leaf_node.state, actions=self.get_action_path(leaf_node)))
            
            # Generate all possible actions for the given state
            actions = self.get_actions(leaf_node.state)
            
            # Create search nodes from the generated actions
            for action in actions:
                # Generate a new state from the given action
                new_state = self.get_result(leaf_node.state, action)
                
                # Create a new search node with the created state and add it to the frontier
                frontier.insert(SearchNode(new_state, leaf_node, action))
    
    
    def id_dfts(self):
        """Performs a Iterative Deepening Depth-First Tree Search (ID-DFTS) on the puzzle's search space 
        starting at the initial state.
        
        Returns a DLSResult class instance containing a solution member with the final state and 
        a list of actions signifying the path from initial state to goal state, if a solution was 
        found. Otherwise, a DLSResult class instance signifying a search failure is returned.
        """
        
        def dls(node, limit):
            """Recursively performs a Depth Limited Search (DLS) on the puzzle's search space
            starting at the given node with given limit.
            
            Returns a DLSResult class instance that contains the problem solution, a flag
            indicating the cutoff was reached, or a flag indicating a search failure.
            """
            if self.check_goal_state(node.state):
                # Search success
                # Return final state and list of actions along path to the goal
                #  as part of the Solution portion of the DLSResult class
                return DLSResult(solution=Solution(final_state=node.state, actions=self.get_action_path(node)))
            
            elif limit == 0:
                # The cutoff has been reached
                return DLSResult(cutoff=True)
                
            else:
                cutoff_occurred = False
                
                # Generate all possible actions for the given state
                actions = self.get_actions(node.state)
            
                for action in actions:
                    # Apply this action to the current state to get the new state
                    new_state = self.get_result(node.state, action)
                    
                    # Create a new child search node with the new state and action
                    child_node = SearchNode(new_state, node, action)
                    
                    # Recursively call DLS on the child node with a reduced limit
                    result = dls(child_node, limit - 1)
                    
                    if result.cutoff:
                        # A cutoff occurred
                        cutoff_occurred = True
                    
                    elif not result.failure:
                        # Search success
                        return result
                
                if cutoff_occurred:
                    # A cutoff occurred
                    return DLSResult(cutoff=True)
                
                else:
                    # This search has failed
                    return DLSReturn(failure=True)


        print('Performing ID-DFTS\n')

        # Iterate through depths from 0 to infinity
        for depth in count(0):
            print('Trying depth', depth)

            # Get the DLS result for this depth
            result = dls(SearchNode(self.initial_state), depth)
            
            if not result.cutoff:
                # A solution has been found or a search failure has ocurred
                # Return the result
                return result
    
    
    def grbefgs(self):
        """Performs a Greedy Best-First Graph Search (GrBeFGS) on the puzzle's 
        search space starting at the initial state.
        
        Returns a GenericResult instance containing a solution with final state and a 
        list of actions signifying the path from initial state to goal state if a solution 
        can be found. If a solution cannot be found, a GenericResult class instance indicating 
        a search failure is returned.
        """
        print('Performing GrBeFGS\n')

        frontier = PriorityFrontier()

        initial_heuristic = self.get_heuristic(self.initial_state)
        initial_node = SearchNode(self.initial_state)
        frontier.insert(initial_node, initial_heuristic)

        visited_nodes = set()
        
        while True:
            if frontier.is_empty():
                # Search failure
                return GenericResult(failure=True)
            
            # Get the next leaf node from the frontier
            leaf_node = frontier.pop()
            
            # Add this node to the visited nodes set
            visited_nodes.add(leaf_node)
            
            # Check for the goal state
            if self.check_goal_state(leaf_node.state):
                # Search success
                # Return final state and list of actions along path to the goal
                #  as part of the GenericResult class solution member
                return GenericResult(solution=Solution(final_state=leaf_node.state, actions=self.get_action_path(leaf_node)))
            
            # Generate all possible actions for the given state
            actions = self.get_actions(leaf_node.state)
            
            # Create search nodes from the generated actions
            for action in actions:
                # Generate a new state from the given action
                new_state = self.get_result(leaf_node.state, action)
                
                # Get the new state's heuristic
                new_heuristic = self.get_heuristic(new_state)

                # Create a new search node with the created state
                new_node = SearchNode(new_state, leaf_node, action)
                
                # If this node has already been visited, ignore it
                if new_node in visited_nodes:
                    continue

                # Check for any nodes with the same state as new_state and with better h values that 
                #  have yet to be visited in the frontier before adding new_node
                if new_node in frontier:
                    frontier_node = frontier.peek_node(new_node)
                    frontier_heuristic = self.get_heuristic(frontier_node.state)

                    if frontier_heuristic <= new_heuristic:
                        # The original heuristic was less than or equal to the new node
                        # Disregard the new node
                        continue
                    
                    else:
                        # The new node's heuristic is larger
                        # Remove the original node from the frontier
                        frontier.remove_node(frontier_node)
                        
                # Add the new node to the frontier
                frontier.insert(new_node, new_heuristic)


    def a_star_gs(self):
        """Performs a A* Graph Search (A*GS) on the puzzle's search space starting at 
        the initial state.
        
        Returns an AStarResult instance containing a solution with final state and a 
        list of actions signifying the path from initial state to goal state if a solution 
        can be found. This includes the number of expanded nodes 
        and the max depth reached by the algorithm, which are used in 
        calculating the effective branching factor. If a solution cannot be found, 
        an AStarResult class instance indicating a search failure is returned.
        """
        print('Performing A*GS\n')

        frontier = PriorityFrontier()

        initial_node = SearchNode(self.initial_state)
        initial_heuristic = self.get_heuristic(self.initial_state) + initial_node.path_cost
        frontier.insert(initial_node, initial_heuristic)

        visited_nodes = set()
        
        num_expanded_nodes = 0
        
        while True:
            if frontier.is_empty():
                # Search failure
                print('Empty frontier.')
                return AStarResult(failure=True)
            
            # Get the next leaf node from the frontier
            leaf_node = frontier.pop()
            
            if not leaf_node:
                # Search failure
                print('Popped all the frontier nodes.')
                return AStarResult(failure=True)
            
            # Check for the goal state
            if self.check_goal_state(leaf_node.state):
                # Search success
                # Return final state and list of actions along path to the goal
                #  as part of the AStarResult class solution member
                action_path = self.get_action_path(leaf_node)
                return AStarResult(solution=Solution(final_state=leaf_node.state, actions=action_path), 
                    num_expanded_nodes=num_expanded_nodes, max_depth=len(action_path) - 1)

            # Add this node to the visited nodes set
            visited_nodes.add(leaf_node)
            
            # Generate all possible actions for the given state
            actions = self.get_actions(leaf_node.state)
            
            # Create search nodes from the generated actions
            for action in actions:
                # Generate a new state from the given action
                new_state = self.get_result(leaf_node.state, action)
                
                # Create a new search node with the created state
                new_node = SearchNode(new_state, leaf_node, action, path_cost=leaf_node.path_cost + 1)
                
                num_expanded_nodes += 1

                # If this node has already been visited, ignore it
                if new_node in visited_nodes:
                    continue

                # Get the new node's heuristic
                new_heuristic = self.get_heuristic(new_state) + new_node.path_cost
                
                # Check for any nodes with the same state as new_state and with better heuristic values that 
                #  have yet to be visited in the frontier before adding new_node
                if new_node in frontier:
                    frontier_node = frontier.peek_node(new_node)
                    frontier_heuristic = frontier.peek_heuristic(new_node)

                    if frontier_heuristic <= new_heuristic:
                        # The original heuristic was less than or equal to the new node
                        # Disregard the new node
                        continue
                    
                    else:
                        # The new node's heuristic is larger
                        # Remove the original node from the frontier
                        frontier.remove_node(frontier_node)

                # Add the new node to the frontier
                frontier.insert(new_node, new_heuristic)


    def get_heuristic(self, state):
        """Returns the heuristic for the given state."""

        def get_manhattan_distance(coord_a, coord_b):
            """Returns the manhattan distance between coord_a and coord_b."""
            return abs(coord_a.x - coord_b.x) + abs(coord_a.y - coord_b.y)

        
        def get_num_obstacles(coord_a, coord_b):
            """Returns the number of obstacles (wriggler segments or walls) between
            coord_a and coord_b.
            
            This function assumes that coord_b is larger (in either/both x and y)
            than coord_a.
            """
            obstacle_count = 0
            
            for x in range(coord_a.x, coord_b.x + 1):
                for y in range(coord_a.y, coord_b.y + 1):
                    coord = Coordinate(x, y)
                    if coord in self.wall_coords or coord in state:
                        obstacle_count += 1
            
            return obstacle_count


        head_coord = state.wriggler_list[0].get_head()
        tail_coord = state.wriggler_list[0].get_tail()
        
        head_manhattan_distance = get_manhattan_distance(head_coord, self.goal_coord)
        tail_manhattan_distance = get_manhattan_distance(tail_coord, self.goal_coord)
        
        # Calculate and return heuristic value depending on which heuristic to use
        if self.heuristic == Heuristic.MANHATTAN_DIST:
            # Return the shortest Manhattan distance of wriggler0's tail or head to the goal
            return min(head_manhattan_distance, tail_manhattan_distance)
        
        else: # self.heuristic == Heuristic.NUM_OBSTACLES:
            # Return the number of obstacles between wriggler0's tail/head to the goal
            # The tail/head is selected based on which is closer to the goal
            if head_manhattan_distance <= tail_manhattan_distance:
                # The head is closer or the same distance away
                return get_num_obstacles(head_coord, self.goal_coord)
            
            else:
                # The tail is closer
                return get_num_obstacles(tail_coord, self.goal_coord)


    def get_action_path(self, node):
        """Returns a list of actions (in chronological order)
        from the leaf node to the given node.
        """
        action_path = []
        
        while node.parent_node:
            # Add this action to the action path
            action_path.append(node.action)
            
            # Reset node's value to the node's parent to save the parent's action
            #  in the next iteration
            node = node.parent_node
        
        # Reverse the order of action_path so that actions appear in the order of 
        #  initial state to goal state
        return action_path[::-1]
