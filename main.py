import pygame

from sokoban import solve_game

if __name__ == '__main__':
    solve_game()

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
