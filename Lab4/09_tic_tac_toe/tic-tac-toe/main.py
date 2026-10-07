"""
Tic-Tac-Toe

Run with: python main.py

Click a cell to place your symbol.
"""

import pygame

from game.game_engine import GameEngine
from game.renderer import WINDOW_SIZE


def main():
    pygame.init()

    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Tic-Tac-Toe")

    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 18)

    engine = GameEngine()

    running = True

    while running:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not engine.handle_control_click(event.pos):
                    engine.handle_click(event.pos)

            elif event.type == pygame.KEYDOWN:
                engine.handle_keydown(event.key)

        engine.draw(screen, font)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()