import subprocess

# Define the command template and the arguments
command_template = 'echo'  # Replace 'echo' with your desired command
arguments = ['arg1', 'arg2', 'arg3']  # Replace with your arguments

# Number of repetitions
num_repetitions = 20

def run_command(command, args, repetitions):
    for arg in args:
        for _ in range(repetitions):
            # Construct the full command
            full_command = [command, arg]
            try:
                # Execute the command
                result = subprocess.run(full_command, capture_output=True, text=True, check=True)
                print(f"Command executed: {result.args}")
                print(f"Output: {result.stdout.strip()}")
            except subprocess.CalledProcessError as e:
                print(f"Error executing command: {e}")
                print(f"Command: {e.cmd}")
                print(f"Output: {e.output}")
                print(f"Error: {e.stderr}")

if __name__ == "__main__":
    run_command(command_template, arguments, num_repetitions)
