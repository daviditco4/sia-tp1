import math

from PriorityQueue import PriorityQueue


def _sum_each_box_to_nearest_goal_ignoring_walls(method):
    min_dist_cache = {}

    def calc(matrix):
        boxes_position = matrix.get_boxes_position()
        goal_position = matrix.get_goals_position()
        key = (' '.join([str(p[0]) + ',' + str(p[1]) for p in boxes_position]),
               ' '.join([str(p[0]) + ',' + str(p[1]) for p in goal_position]))
        if key in min_dist_cache:
            return min_dist_cache[key]
        else:
            total = 0
            for bp in boxes_position:
                total += min([method(bp, tp) for tp in goal_position] or [0])
            min_dist_cache[key] = total
            return total

    return calc


class Searcher:
    cache = {}
    costs = {
        'uniform': lambda _: 1,
        'cost2': lambda action: 1 if action == 'move' else 2,
        'cost3': lambda action: 1 if action == 'move' else 2 if action == 'push' else 3
    }
    heuristics = {
        'none': lambda _: 0,
        'manhattan': _sum_each_box_to_nearest_goal_ignoring_walls(lambda a, b: abs(a[0] - b[0]) + abs(a[1] - b[1])),
        'euclidean': _sum_each_box_to_nearest_goal_ignoring_walls(
            lambda a, b: math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)),
    }

    def bfs(self, starting_matrix, cache):
        return self.astar(starting_matrix, heuristic='none', cache=cache)

    def astar(self, starting_matrix, cache, cost='uniform', heuristic='manhattan', max_cost=1000):
        h = self.heuristics[heuristic]
        c = self.costs[cost]
        queue = PriorityQueue()
        action_sequence_cache = {str(starting_matrix): ''}
        starting_matrix.heuristic = h(starting_matrix)
        queue.add_item(starting_matrix, starting_matrix.heuristic, starting_matrix.heuristic)
        while not queue.is_empty():
            matrix_cost_heuristic, matrix = queue.pop_item()
            action_sequence = action_sequence_cache[str(matrix)]
            cache[str(matrix)] = len(action_sequence)
            if matrix.is_win():
                return action_sequence, len(cache)
            if matrix_cost_heuristic > max_cost:
                continue
            for action, action_cost in matrix.get_possible_actions():
                successor = matrix.successor(action)
                if str(successor) in cache:
                    continue
                if not str(successor) in action_sequence_cache or len(action_sequence_cache[str(successor)]) > len(
                        action_sequence) + 1:
                    action_sequence_cache[str(successor)] = action_sequence + action
                successor.heuristic = h(successor)
                queue.add_item(successor,
                               matrix_cost_heuristic - matrix.heuristic + c(action_cost) + successor.heuristic,
                               successor.heuristic)
        return '', len(cache)
