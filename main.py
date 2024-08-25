import sys
import optparse

import pygame

from sokoban import solve_game


def parse_arguments():
    usage_str = '''
    USAGE:      python3 sokoban.py <options>
    EXAMPLES:   (1) python3 sokoban.py -b boards/my_board.txt
    '''
    parser = optparse.OptionParser(usage_str)

    parser.add_option('-b', '--board', dest='board', type='str', help='The board to solve', metavar='board')
    parser.add_option('-a', '--algorithm', dest='algorithm', type='str', help='The search algorithm',
                      metavar='algorithm', default='astar')
    parser.add_option('-t', '--timeout', dest='timeout', type='int', help="The method's timeout in seconds",
                      metavar='timeout', default=100)
    parser.add_option('-c', '--cost', dest='cost', type='str', help='The cost function to use', metavar='cost',
                      default='uniform')
    parser.add_option('-s', '--heuristic', dest='heuristic', type='str', help='The heuristic function to use',
                      metavar='heuristic', default='manhattan')
    options, other_junk = parser.parse_args(sys.argv[1:])
    if len(other_junk) != 0:
        raise Exception('Command option(s) not understood: ' + str(other_junk))
    return options


if __name__ == '__main__':
    args = parse_arguments()
    solve_game(args)

    pygame.init()

    screen = pygame.display.set_mode((1280, 720))

    clock = pygame.time.Clock()

    while True:
        # Process player inputs.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

        screen.fill('purple')  # Fill the display with a solid color

        pygame.display.flip()  # Refresh on-screen display
        clock.tick(60)  # wait until next frame (at 60 FPS)
