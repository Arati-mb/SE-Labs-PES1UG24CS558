"""
renderer: all pygame drawing lives here, kept separate from game logic.
"""

import pygame

WIDTH, HEIGHT = 400, 560

BOARD_SIZE = 360
CELL_SIZE = BOARD_SIZE // 3
BOARD_TOP = 100

WINDOW_SIZE = (WIDTH, HEIGHT)

COLOR_BG = (245, 245, 245)
COLOR_LINE = (60, 60, 60)
COLOR_X = (200, 60, 60)
COLOR_O = (60, 100, 200)
COLOR_TEXT = (30, 30, 30)

COLOR_BUTTON = (220, 220, 220)
COLOR_BUTTON_SELECTED = (180, 210, 240)
COLOR_BUTTON_BORDER = (80, 80, 80)


# -------------------------
# Task 4 control rectangles
# -------------------------

START_X_BUTTON = pygame.Rect(105, 65, 60, 28)
START_O_BUTTON = pygame.Rect(170, 65, 60, 28)

RESTART_BUTTON = pygame.Rect(80, 475, 115, 35)
RESET_MATCH_BUTTON = pygame.Rect(205, 475, 115, 35)


def board_pos_to_cell(pos):
    x, y = pos

    y -= BOARD_TOP

    if not (0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE):
        return None

    col = x // CELL_SIZE
    row = y // CELL_SIZE

    return int(row), int(col)


def draw_board(surface, board):
    surface.fill(COLOR_BG)

    for i in range(1, 3):
        pygame.draw.line(
            surface,
            COLOR_LINE,
            (i * CELL_SIZE, BOARD_TOP),
            (i * CELL_SIZE, BOARD_TOP + BOARD_SIZE),
            3
        )

        pygame.draw.line(
            surface,
            COLOR_LINE,
            (0, BOARD_TOP + i * CELL_SIZE),
            (BOARD_SIZE, BOARD_TOP + i * CELL_SIZE),
            3
        )

    for r in range(3):
        for c in range(3):
            symbol = board[r][c]

            if symbol is None:
                continue

            center = (
                c * CELL_SIZE + CELL_SIZE // 2,
                BOARD_TOP + r * CELL_SIZE + CELL_SIZE // 2
            )

            if symbol == 'X':
                offset = CELL_SIZE // 3

                pygame.draw.line(
                    surface,
                    COLOR_X,
                    (center[0] - offset, center[1] - offset),
                    (center[0] + offset, center[1] + offset),
                    6
                )

                pygame.draw.line(
                    surface,
                    COLOR_X,
                    (center[0] + offset, center[1] - offset),
                    (center[0] - offset, center[1] + offset),
                    6
                )

            else:
                pygame.draw.circle(
                    surface,
                    COLOR_O,
                    center,
                    CELL_SIZE // 3,
                    6
                )


def draw_text(surface, font, text, pos, color=COLOR_TEXT):
    surface.blit(
        font.render(text, True, color),
        pos
    )


def draw_scoreboard(surface, font, x_wins, o_wins, draws):
    text = (
        f"X Wins: {x_wins}   "
        f"O Wins: {o_wins}   "
        f"Draws: {draws}"
    )

    draw_text(surface, font, text, (10, 35))


def draw_button(surface, font, rect, text, selected=False):
    color = (
        COLOR_BUTTON_SELECTED
        if selected
        else COLOR_BUTTON
    )

    pygame.draw.rect(
        surface,
        color,
        rect
    )

    pygame.draw.rect(
        surface,
        COLOR_BUTTON_BORDER,
        rect,
        2
    )

    label = font.render(
        text,
        True,
        COLOR_TEXT
    )

    label_rect = label.get_rect(
        center=rect.center
    )

    surface.blit(label, label_rect)


def draw_controls(surface, font, starting_player):
    draw_text(
        surface,
        font,
        "Next start:",
        (10, 70)
    )

    draw_button(
        surface,
        font,
        START_X_BUTTON,
        "X",
        selected=(starting_player == 'X')
    )

    draw_button(
        surface,
        font,
        START_O_BUTTON,
        "O",
        selected=(starting_player == 'O')
    )

    draw_button(
        surface,
        font,
        RESTART_BUTTON,
        "Restart Round"
    )

    draw_button(
        surface,
        font,
        RESET_MATCH_BUTTON,
        "Reset Match"
    )


def control_at_pos(pos):
    if START_X_BUTTON.collidepoint(pos):
        return "start_x"

    if START_O_BUTTON.collidepoint(pos):
        return "start_o"

    if RESTART_BUTTON.collidepoint(pos):
        return "restart"

    if RESET_MATCH_BUTTON.collidepoint(pos):
        return "reset_match"

    return None


def draw_banner(surface, font, text):
    surf = font.render(
        text,
        True,
        (180, 40, 40)
    )

    rect = surf.get_rect(
        center=(
            surface.get_width() // 2,
            530
        )
    )

    surface.blit(surf, rect)