import copy


def _update_valid(item, move, get_two_step):
    if item not in '#$*':
        return move, 'move'
    if item in '$*' and get_two_step() not in '#$*':
        return (move, 'push') if item == '$' else (move, 'push_out')
    return None


def _successor(matrix, direction):
    x, y = matrix.get_player_position()

    match direction:
        case 'L':
            versor = (0, -1)
        case 'R':
            versor = (0, 1)
        case 'U':
            versor = (-1, 0)
        case 'D':
            versor = (1, 0)
        case _:
            versor = None
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
    _size = (0, 0)
    _string = ''
    _heuristic = None
    _moves = None
    _actions = None

    def __hash__(self):
        return hash(str(self))

    def __str__(self):
        self._string = self._string or '\n'.join([''.join(i) for i in self])
        return self._string

    @property
    def size(self):
        return self._size

    @property
    def heuristic(self):
        return self._heuristic

    @size.setter
    def size(self, value):
        self._size = value

    @heuristic.setter
    def heuristic(self, value):
        self._heuristic = value

    def get_player_position(self):
        for i in range(len(self)):
            for j in range(len(self[i])):
                if self[i][j] in '@+':
                    return j, i

    def get_boxes_position(self):
        boxes = []
        for i in range(len(self)):
            for j in range(len(self[i])):
                if self[i][j] in '$*':
                    boxes.append([j, i])
        return boxes

    def get_goals_position(self):
        goals = []
        for i in range(len(self)):
            for j in range(len(self[i])):
                if self[i][j] in '+*.':
                    goals.append([j, i])
        return goals

    def is_win(self):
        for row in self:
            for col in row:
                if col == '$':
                    return False
        return True

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
    _matrix = Matrix()
    matrix_history = None

    def __init__(self, board_file_path):
        if not board_file_path:
            return

        max_row_length = 0
        with open(board_file_path, 'r') as f:
            for row in f.read().splitlines():
                self._matrix.append(list(row))
                if len(row) > max_row_length:
                    max_row_length = len(row)

        self._matrix._size = (max_row_length, len(self._matrix))

    @property
    def matrix(self):
        return self._matrix
