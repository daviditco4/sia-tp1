import math  # Importing the math module for mathematical operations

from PriorityQueue import PriorityQueue  # Importing the PriorityQueue class from the PriorityQueue module


def _sum_each_box_to_nearest_goal_ignoring_walls(method):
    min_dist_cache = {}  # Initialize a cache for minimum distances

    def calc(matrix):
        boxes_position = matrix.get_boxes_position()  # Get the positions of all boxes
        goal_position = matrix.get_goals_position()  # Get the positions of all goals
        key = (' '.join([str(p[0]) + ',' + str(p[1]) for p in boxes_position]),
               ' '.join([str(p[0]) + ',' + str(p[1]) for p in goal_position]))  # Create a cache key
        if key in min_dist_cache:
            return min_dist_cache[key]  # Return cached value if available
        else:
            total = 0
            for b in boxes_position:
                total += min([method(b, t) for t in goal_position] or [0])  # Calculate total distance
            min_dist_cache[key] = total  # Cache the calculated value
            return total

    return calc


class Searcher:
    cache = {}  # Initialize a cache for search results
    costs = {
        'uniform': lambda _: 1,  # Uniform cost function
        'cost2': lambda action: 1 if action == 'move' else 2,  # Cost function with different costs for moves and pushes
        'cost3': lambda action: 1 if action == 'move' else 2 if action == 'push' else 3  # Cost function with different costs for moves, pushes, and push_outs
    }
    heuristics = {
        'none': lambda _: 0,  # No heuristic
        'manhattan': _sum_each_box_to_nearest_goal_ignoring_walls(lambda a, b: abs(a[0] - b[0]) + abs(a[1] - b[1])),  # Manhattan distance heuristic
        'euclidean': _sum_each_box_to_nearest_goal_ignoring_walls(
            lambda a, b: math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)),  # Euclidean distance heuristic
    }

    def bfs(self, starting_matrix, cache):
        return self.astar(starting_matrix, heuristic='none', cache=cache)  # Perform BFS using A* with no heuristic

    def astar(self, starting_matrix, cache, cost='uniform', heuristic='manhattan', max_cost=1000):
        h = self.heuristics[heuristic]  # Get the heuristic function
        c = self.costs[cost]  # Get the cost function
        queue = PriorityQueue()  # Initialize the priority queue
        action_sequence_cache = {str(starting_matrix): ''}  # Initialize the action sequence cache
        starting_matrix.heuristic = h(starting_matrix)  # Calculate the heuristic for the starting matrix
        queue.add_item(starting_matrix, starting_matrix.heuristic, starting_matrix.heuristic)  # Add the starting matrix to the queue
        while not queue.is_empty():
            matrix_cost_heuristic, matrix = queue.pop_item()  # Pop the matrix with the lowest cost from the queue
            action_sequence = action_sequence_cache[str(matrix)]  # Get the action sequence for the current matrix
            cache[str(matrix)] = len(action_sequence)  # Cache the length of the action sequence
            if matrix.is_win():
                print(matrix)
                print('Win')
                return action_sequence, len(cache)  # Return the action sequence and the cache size if the goal is reached
            if matrix_cost_heuristic > max_cost:
                print('Reached max cost')
                continue  # Skip if the cost exceeds the maximum allowed cost
            for (action, action_cost) in matrix.get_possible_actions():
                successor = matrix.successor(action)  # Get the successor matrix for the action
                if str(successor) in cache:
                    continue  # Skip if the successor is already in the cache
                if not str(successor) in action_sequence_cache or len(action_sequence_cache[str(successor)]) > len(
                        action_sequence) + 1:
                    action_sequence_cache[str(successor)] = action_sequence + action  # Update the action sequence cache
                successor.heuristic = h(successor)  # Calculate the heuristic for the successor
                queue.add_item(successor,
                               matrix_cost_heuristic - matrix.heuristic + c(action_cost) + successor.heuristic,
                               successor.heuristic)  # Add the successor to the queue with updated cost
        return '', len(cache)  # Return an empty action sequence and the cache size if no solution is found

    def dfs(self, starting_matrix, cache):
        stack = [starting_matrix]  # Initialize the stack with the starting matrix
        action_sequence_cache = {str(starting_matrix): ''}  # Initialize the action sequence cache
        while stack:
            matrix = stack.pop()  # Pop the last matrix from the stack
            action_sequence = action_sequence_cache[str(matrix)]  # Get the action sequence for the current matrix
            cache[str(matrix)] = len(action_sequence)  # Cache the length of the action sequence
            if matrix.is_win():
                print(matrix)
                print('Win')
                return action_sequence, len(cache)  # Return the action sequence and the cache size if the goal is reached
            for (action, action_cost) in matrix.get_possible_actions():
                successor = matrix.successor(action)  # Get the successor matrix for the action
                if str(successor) in cache:
                    continue  # Skip if the successor is already in the cache
                if not str(successor) in action_sequence_cache or len(action_sequence_cache[str(successor)]) > len(
                        action_sequence) + 1:
                    action_sequence_cache[str(successor)] = action_sequence + action  # Update the action sequence cache
                stack.append(successor)  # Push the successor onto the stack
        return '', len(cache)  # Return an empty action sequence and the cache size if no solution is found