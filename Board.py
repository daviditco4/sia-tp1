import copy  # Importing the copy module for deep copying objects


def _update_valid(item, move, get_two_step):
    # Check if the item is not a wall or box
    if item not in '#$*':
        return move, 'move'  # Return move and action type 'move'
    # Check if the item is a box and the next step is not a wall or box
    if item in '$*' and get_two_step() not in '#$*':
        return (move, 'push') if item == '$' else (move, 'push_out')  # Return move and action type based on item
    return None  # Return None if the move is not valid


def _successor(matrix, direction):
    # Get the player's current position
    x, y = matrix.get_player_position()

    # Determine the direction vector based on the input direction
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

    # Get the items in the next step and two steps ahead
    step = matrix[y + versor[0]][x + versor[1]]
    two_step = matrix[y + 2 * versor[0]][x + 2 * versor[1]]

    # Update the matrix based on the step and two_step items
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
    _size = (0, 0)  # Initialize the size of the matrix
    _string = ''  # Initialize the string representation of the matrix
    _heuristic = None  # Initialize the heuristic value
    _moves = None  # Initialize the moves
    _actions = None  # Initialize the actions

    def __hash__(self):
        return hash(str(self))  # Return the hash of the string representation of the matrix

    def __str__(self):
        self._string = self._string or '\n'.join([''.join(i) for i in self])  # Generate the string representation
        return self._string

    @property
    def size(self):
        return self._size  # Return the size of the matrix

    @property
    def heuristic(self):
        return self._heuristic  # Return the heuristic value

    @size.setter
    def size(self, value):
        self._size = value  # Set the size of the matrix

    @heuristic.setter
    def heuristic(self, value):
        self._heuristic = value  # Set the heuristic value

    def get_player_position(self):
        # Find and return the player's position in the matrix
        for i in range(len(self)):
            for j in range(len(self[i])):
                if self[i][j] in '@+':
                    return j, i

    def get_boxes_position(self):
        # Find and return the positions of all boxes in the matrix
        boxes = []
        for i in range(len(self)):
            for j in range(len(self[i])):
                if self[i][j] in '$*':
                    boxes.append([j, i])
        return boxes

    def get_goals_position(self):
        # Find and return the positions of all goals in the matrix
        goals = []
        for i in range(len(self)):
            for j in range(len(self[i])):
                if self[i][j] in '+*.':
                    goals.append([j, i])
        return goals

    def is_win(self):
        # Check if all boxes are on goals
        for row in self:
            for col in row:
                if col == '$':
                    return False
        return True

    def get_possible_actions(self):
        # Get the player's current position
        x, y = self.get_player_position()

        # Determine possible moves and their costs
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
        # Generate the successor matrix based on the direction
        if perform_on_self:
            return _successor(self, direction)
        matrix = copy.deepcopy(self)
        _successor(matrix, direction)
        matrix._string = None
        return matrix


class Board:
    _matrix = Matrix()  # Initialize the matrix
    matrix_history = None  # Initialize the matrix history

    def __init__(self, board_file_path):
        if not board_file_path:
            return

        max_row_length = 0  # Initialize the maximum row length
        with open(board_file_path, 'r') as f:
            for row in f.read().splitlines():
                self._matrix.append(list(row))  # Append each row to the matrix
                if len(row) > max_row_length:
                    max_row_length = len(row)  # Update the maximum row length

        self._matrix._size = (max_row_length, len(self._matrix))  # Set the size of the matrix

    @property
    def matrix(self):
        return self._matrix  # Return the matrix