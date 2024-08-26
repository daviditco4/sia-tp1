import sys  # Importing the sys module for system-specific parameters and functions
import optparse  # Importing the optparse module for parsing command-line options

import pygame  # Importing the pygame module for game development

from sokoban import solve_game  # Importing the solve_game function from the sokoban module


def parse_arguments():
    usage_str = '''
    USAGE:      python3 sokoban.py <options>
    EXAMPLES:   (1) python3 sokoban.py -b boards/my_board.txt
    '''
    parser = optparse.OptionParser(usage_str)  # Creating an OptionParser object with usage instructions

    # Adding command-line options for the parser
    parser.add_option('-b', '--board', dest='board', type='str', help='The board to solve', metavar='board')
    parser.add_option('-a', '--algorithm', dest='algorithm', type='str', help='The search algorithm',
                      metavar='algorithm', default='astar')
    parser.add_option('-t', '--timeout', dest='timeout', type='int', help="The method's timeout in seconds",
                      metavar='timeout', default=10000)
    parser.add_option('-c', '--cost', dest='cost', type='str', help='The cost function to use', metavar='cost',
                      default='uniform')
    parser.add_option('-s', '--heuristic', dest='heuristic', type='str', help='The heuristic function to use',
                      metavar='heuristic', default='manhattan')

    # Parsing the command-line arguments
    options, other_junk = parser.parse_args(sys.argv[1:])

    # Raising an exception if there are unrecognized command-line arguments
    if len(other_junk) != 0:
        raise Exception('Command option(s) not understood: ' + str(other_junk))

    return options  # Returning the parsed options


if __name__ == '__main__':
    args = parse_arguments()  # Parsing command-line arguments
    solve_game(args)  # Calling the solve_game function with the parsed arguments

    pygame.init()  # Initializing all imported pygame modules

    screen = pygame.display.set_mode((1280, 720))  # Setting up the display window with a resolution of 1280x720

    clock = pygame.time.Clock()  # Creating a Clock object to manage the frame rate

    while True:
        # Processing player inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Checking if the quit event is triggered
                pygame.quit()  # Uninitializing all pygame modules
                raise SystemExit  # Exiting the program

        screen.fill('purple')  # Filling the display with a solid color (purple)

        pygame.display.flip()  # Updating the display to show the new frame
        clock.tick(60)  # Pausing to maintain a frame rate of 60 FPS