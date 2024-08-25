import csv
import multiprocessing
import pathlib
import time

from Board import Board
from Searcher import Searcher

board = Board('')


def _solve_internal(cache, algorithm, cost, heuristic, ret):
    searcher = Searcher()

    match algorithm:
        case 'bfs':
            moves = searcher.bfs(board.matrix, cache)
        case 'astar':
            moves = searcher.astar(board.matrix, cache=cache, cost=cost, heuristic=heuristic)
        case _:
            moves = None

    ret.put(moves)


def _solve(args):
    ret = multiprocessing.Queue()
    cache = {}

    p = multiprocessing.Process(target=_solve_internal, args=(cache, args.algorithm, args.cost, args.heuristic, ret))
    starting_time = time.time()
    p.start()
    p.join(args.timeout)

    action_sequence, nodes_expanded = ret.get() or '', None
    log_file_path = args.algorithm + '.csv'
    log_path = pathlib.Path(log_file_path)
    info = {'Algorithm': args.algorithm, 'Board': pathlib.Path(args.board).name,
            'ElapsedSeconds': time.time() - starting_time, 'AmountOfMovesToWin': len(action_sequence) or None,
            'NodesExpanded': nodes_expanded}
    with open(log_file_path, mode='a', newline='') as log_file:
        writer = csv.DictWriter(log_file, fieldnames=list(info.keys()))
        if not (log_path.exists() and log_path.stat().st_size):
            writer.writeheader()
        writer.writerow(info)

    return action_sequence


def solve_game(args):
    global board
    board = Board(args.board)

    _solve(args)
