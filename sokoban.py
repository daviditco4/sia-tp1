import csv  # Importing the csv module for CSV file operations
import multiprocessing  # Importing the multiprocessing module for parallel processing
import pathlib  # Importing the pathlib module for filesystem path operations
import time  # Importing the time module for time-related functions

from Board import Board  # Importing the Board class from the Board module
from Searcher import Searcher  # Importing the Searcher class from the Searcher module


def _solve_internal(matrix, cache, algorithm, cost, heuristic, ret):
    searcher = Searcher()  # Creating an instance of the Searcher class

    # Matching the algorithm to the corresponding search method
    match algorithm:
        case 'bfs':
            moves = searcher.bfs(matrix, cache)  # Performing BFS search
        case 'astar':
            moves = searcher.astar(matrix, cache=cache, cost=cost, heuristic=heuristic)  # Performing A* search
        case _:
            moves = None  # Default case if the algorithm is not recognized

    ret.put(moves)  # Putting the result in the return queue


def _solve(matrix, args):
    ret = multiprocessing.Queue()  # Creating a multiprocessing queue for the result
    cache = {}  # Initializing the cache

    # Creating a new process to solve the puzzle
    p = multiprocessing.Process(target=_solve_internal, args=(matrix, cache, args.algorithm, args.cost, args.heuristic, ret))
    starting_time = time.time()  # Recording the start time
    p.start()  # Starting the process
    p.join(args.timeout)  # Joining the process with a timeout

    # Retrieving the result from the queue
    action_sequence, nodes_expanded = ret.get() if not ret.empty() else ('', 'N/A')
    log_file_path = args.algorithm + '.csv'  # Creating the log file path
    log_path = pathlib.Path(log_file_path)  # Creating a Path object for the log file
    info = {'Algorithm': args.algorithm, 'Board': pathlib.Path(args.board).name,
            'ElapsedSeconds': time.time() - starting_time, 'AmountOfMovesToWin': len(action_sequence) or 'N/A',
            'NodesExpanded': nodes_expanded}  # Creating the log information dictionary
    with open(log_file_path, mode='a', newline='') as log_file:
        writer = csv.DictWriter(log_file, fieldnames=list(info.keys()))  # Creating a CSV DictWriter
        if not (log_path.exists() and log_path.stat().st_size):
            writer.writeheader()  # Writing the header if the file is empty
        writer.writerow(info)  # Writing the log information

    return action_sequence  # Returning the action sequence


def solve_game(args):
    board = Board(args.board)  # Creating an instance of the Board class with the specified board file

    print('Solved: ' + _solve(board.matrix, args))  # Solving the game and printing the result