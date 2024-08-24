import math


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
        return self.astar(starting_matrix, cost='uniform', heuristic='none', max_cost=500, cache=cache)

    def astar(self, starting_matrix, cache, cost='uniform', heuristic='manhattan', max_cost=500):
        h = self.heuristics[heuristic]
        c = self.costs[cost]

        return '', 0
