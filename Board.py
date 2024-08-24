import copy
import sys


def _update_valid(item, move, get_two_step):
    if item not in '#$*':
        return move, 'move'
    if item in '$*' and get_two_step() not in '#$*':
        # We do not like moving blocks out of their respective targets
        return (move, 'push') if item is '$' else (move, 'push_out')
    return None


def _successor(matrix, direction):
    x, y = matrix.get_player_position()
    versor = None

    match direction:
        case 'L':
            versor = (0, -1)
        case 'R':
            versor = (0, 1)
        case 'U':
            versor = (-1, 0)
        case 'D':
            versor = (1, 0)
    step = matrix[y + versor[0]][x + versor[1]]
    two_step = matrix[y + 2 * versor[0]][x + 2 * versor[1]]

    if step == ' ':
        matrix[y + versor[0]][x + versor[1]] = '@'
    elif step == '$':
        if two_step == ' ':
            matrix[y + 2 * versor[0]][x + 2 * versor[1]] = '$'
            matrix[y + versor[0]][x + versor[1]] = '@'
        elif two_step == '.':
            matrix[y + 2 * versor[0]][x + 2 * versor[1]] = '*'
            matrix[y + versor[0]][x + versor[1]] = '@'
    elif step == '*':
        if two_step == ' ':
            matrix[y + 2 * versor[0]][x + 2 * versor[1]] = '$'
            matrix[y + versor[0]][x + versor[1]] = '+'
        elif two_step == '.':
            matrix[y + 2 * versor[0]][x + 2 * versor[1]] = '*'
            matrix[y + versor[0]][x + versor[1]] = '+'
    elif step == '.':
        matrix[y + versor[0]][x + versor[1]] = '+'
    if matrix[y][x] == '+':
        matrix[y][x] = '.'
    else:
        matrix[y][x] = ' '


class Matrix(list):
    _size = [0, 0]
    _string = ''
    _moves = None
    _actions = None

    def get_size(self):
        return self._size

    def get_player_position(self):
        for i in range(0, len(self)):
            for j in range(0, len(self[i])):
                if self[i][j] in '@+':
                    return j, i

    def get_possible_actions(self):
        x, y = self.get_player_position()

        moves = []
        action_cost = _update_valid(self[y][x - 1], 'L', lambda: self[y][x - 2])
        if action_cost is not None:
            moves.append(action_cost)
        action_cost = _update_valid(self[y][x + 1], 'R', lambda: self[y][x + 2])
        if action_cost is not None:
            moves.append(action_cost)
        action_cost = _update_valid(self[y - 1][x], 'U', lambda: self[y - 2][x])
        if action_cost is not None:
            moves.append(action_cost)
        action_cost = _update_valid(self[y + 1][x], 'D', lambda: self[y + 2][x])
        if action_cost is not None:
            moves.append(action_cost)
        return moves

    def successor(self, direction, perform_on_self=False):
        if perform_on_self:
            return _successor(self, direction)
        matrix = copy.deepcopy(self)
        _successor(matrix, direction)
        matrix._string = None
        return matrix


class Board:
    matrix = Matrix()
    matrix_history = None

    def __init__(self):
        with open(sys.argv[1], 'r') as f:
            for row in f.read().splitlines():
                self.matrix.append(list(row))

        max_row_length = 0
        for row in self.matrix:
            row_length = len(row)
            if row_length > max_row_length:
                max_row_length = row_length

        self.matrix.size = [max_row_length, len(self.matrix)]
        self.matrix.width = max_row_length
        self.matrix.height = len(self.matrix)
