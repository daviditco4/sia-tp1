import subprocess

# Define the command template and the arguments
command_template = 'python3'
arguments = ['main.py -b 1.sok -a bfs', 'main.py -b 2.sok -a bfs', 'main.py -b 3.sok -a bfs', 'main.py -b 4.sok -a bfs',
             'main.py -b 1.sok -a dfs', 'main.py -b 2.sok -a dfs', 'main.py -b 3.sok -a dfs', 'main.py -b 4.sok -a dfs',
             'main.py -b 1.sok -a greedy', 'main.py -b 2.sok -a greedy', 'main.py -b 3.sok -a greedy',
             'main.py -b 4.sok -a greedy', 'main.py -b 1.sok -a astar', 'main.py -b 2.sok -a astar',
             'main.py -b 3.sok -a astar', 'main.py -b 4.sok -a astar']

# Number of repetitions
num_repetitions = 20


def run_command(command, args, repetitions):
    for arg in args:
        for _ in range(repetitions):
            # Construct the full command
            full_command = [command_template] + arg.split()
            try:
                # Execute the command
                result = subprocess.run(full_command, capture_output=True, text=True, check=True)
                print(f'Command executed: {result.args}')
                print('Output:')
                print(result.stdout.strip())
            except subprocess.CalledProcessError as e:
                print(f'Error executing command: {e}')
                print(f'Command: {e.cmd}')
                print(f'Output: {e.output}')
                print(f'Error: {e.stderr}')


if __name__ == "__main__":
    run_command(command_template, arguments, num_repetitions)
