# SIA TP1

Implementation of Sokoban based on Python with the pygame library.

## System requirements

* Python 3.10+

## How to use

1. Clone or download this repository in the folder you desire
2. In a new terminal, navigate to the repository using `cd`
3. When you are ready, enter a command as follows:
```sh
python3 sokoban.py -b <board> [-a <algorithm>] [-t <timeout>] [-c <cost>] [-h <heuristic>]
```

### Arguments

* `-b, --board`: The file path to the starting board of the level
* `-a, --algorithm`: The algorithm for computing the solution of the level (currently available ones are
`bfs`, `dfs`, `greedy` and `astar`)
* `-t, --timeout`: The timeout for the execution in seconds
* `-c, --cost`: The function for calculating the cost of the actions (default is `uniform`)
* `-h, --heuristic`: The heuristic for running the algorithm (currently available ones are `none`,
`manhattan` and `euclidean`)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.