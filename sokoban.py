import multiprocessing

from Board import Board
from Searcher import Searcher

board = None


def _solve_internal(cache, method, cost, heuristic, ret):
    searcher = Searcher()
    solution.refresh()
    moves = []
    moves_cache = []

    ret.put(moves_cache)
    # return moves


def _solve(args):
    p = multiprocessing.Process(target=_solve_internal, args=(cache, args.method, args.cost, args.heuristic, ret))
    p.start()

    return ''


def solve_game(args):
    global board
    board = Board()

    moves = _solve(args)
