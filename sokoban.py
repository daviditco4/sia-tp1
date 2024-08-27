import csv
import multiprocessing
import pathlib
import time

from Board import Board
from Searcher import Searcher


def _solve_internal(matrix, cache, algorithm, cost, heuristic, ret):
    searcher = Searcher()

    match algorithm:
        case 'bfs':
            moves = searcher.bfs(matrix, cache)
        case 'dfs':
            moves = searcher.dfs(matrix, cache)
        case 'greedy':
            moves = searcher.greedy(matrix, cache, heuristic=heuristic)
        case 'astar':
            moves = searcher.astar(matrix, cache=cache, cost=cost, heuristic=heuristic)
        case _:
            moves = None

    ret.put(moves)


def _solve(matrix, args):
    ret = multiprocessing.Queue()
    cache = {}

    p = multiprocessing.Process(target=_solve_internal,
                                args=(matrix, cache, args.algorithm, args.cost, args.heuristic, ret))
    starting_time = time.time()
    p.start()
    p.join(args.timeout)

    action_sequence, nodes_expanded, frontier_nodes = ret.get() if not ret.empty() else ('', 'N/A', 'N/A')
    log_file_path = args.algorithm + '.csv'
    log_path = pathlib.Path(log_file_path)
    info = {'Algorithm': args.algorithm, 'Board': pathlib.Path(args.board).stem,
            'ElapsedSeconds': time.time() - starting_time,
            'Heuristic': args.heuristic if args.algorithm == 'greedy' or args.algorithm == 'astar' else 'N/A',
            'AmountOfMovesToWin': len(action_sequence) or 'N/A', 'NodesExpanded': nodes_expanded,
            'FrontierNodes': frontier_nodes}
    with open(log_file_path, mode='a', newline='') as log_file:
        writer = csv.DictWriter(log_file, fieldnames=list(info.keys()))
        if not (log_path.exists() and log_path.stat().st_size):
            writer.writeheader()
        writer.writerow(info)

    return action_sequence


def solve_game(args):
    board = Board(args.board)

    print('Solved: ' + _solve(board.matrix, args))
