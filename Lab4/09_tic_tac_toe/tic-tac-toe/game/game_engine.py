"""
GameEngine: owns the board, turn state, round-end logic,
persistent scoreboard, and starting-player selection.
"""

from game.rules import check_winner, is_board_full
from game.renderer import board_pos_to_cell
from game.ai import choose_move

HUMAN_SYMBOL = 'X'
COMPUTER_SYMBOL = 'O'


class GameEngine:
    def __init__(self):
        # Persistent scoreboard
        self.x_wins = 0
        self.o_wins = 0
        self.draws = 0

        # The selected player starts the NEXT round.
        self.starting_player = HUMAN_SYMBOL

        self._reset_round()

    def _reset_round(self):
        """Reset only the current round and keep the scoreboard."""
        self.board = [[None] * 3 for _ in range(3)]
        self.current_player = self.starting_player
        self.round_over = False
        self.winner = None

        # If O starts, the computer makes the first move automatically.
        self._maybe_take_computer_turn()

    def reset_match(self):
        """Reset the complete match, including the scoreboard."""
        self.x_wins = 0
        self.o_wins = 0
        self.draws = 0

        self.starting_player = HUMAN_SYMBOL

        self._reset_round()

    def set_starting_player(self, symbol):
        """
        Select who will start the NEXT round.

        The current round is not changed.
        """
        if symbol not in (HUMAN_SYMBOL, COMPUTER_SYMBOL):
            return

        self.starting_player = symbol

    def handle_click(self, pos):
        """
        Handle a click on the board.

        Task 3: occupied cells are rejected without changing
        the board, turn, scoreboard, or triggering the computer.
        """
        if self.round_over:
            return

        if self.current_player != HUMAN_SYMBOL:
            return

        cell = board_pos_to_cell(pos)

        if cell is None:
            return

        row, col = cell

        # Task 3: reject occupied cells completely.
        if self.board[row][col] is not None:
            return

        self.board[row][col] = self.current_player

        self.check_round_end()

        if self.round_over:
            return

        self.current_player = COMPUTER_SYMBOL
        self._maybe_take_computer_turn()

    def _maybe_take_computer_turn(self):
        """
        Make the computer move when it is O's turn.

        This also handles the case where O was selected to
        start the next round.
        """
        if self.round_over:
            return

        if self.current_player != COMPUTER_SYMBOL:
            return

        move = choose_move(self.board)

        if move is None:
            return

        row, col = move

        self.board[row][col] = COMPUTER_SYMBOL

        self.check_round_end()

        if self.round_over:
            return

        self.current_player = HUMAN_SYMBOL

    def handle_keydown(self, key):
        """
        Keep R as a keyboard shortcut for restarting the round.
        """
        import pygame

        if key == pygame.K_r:
            self._reset_round()

        elif key == pygame.K_m:
            self.reset_match()

        elif key == pygame.K_x:
            self.set_starting_player(HUMAN_SYMBOL)

        elif key == pygame.K_o:
            self.set_starting_player(COMPUTER_SYMBOL)

    def handle_control_click(self, pos):
        """
        Handle clicks on Task 4 controls.

        Returns True if the click was handled by a control.
        """
        from game import renderer

        control = renderer.control_at_pos(pos)

        if control == "start_x":
            self.set_starting_player(HUMAN_SYMBOL)
            return True

        if control == "start_o":
            self.set_starting_player(COMPUTER_SYMBOL)
            return True

        if control == "restart":
            self._reset_round()
            return True

        if control == "reset_match":
            self.reset_match()
            return True

        return False

    def check_round_end(self):
        # Task 1: winner must always be checked before draw.
        winner = check_winner(self.board)

        if winner:
            self.round_over = True
            self.winner = winner

            # Task 2: update persistent scoreboard.
            if winner == HUMAN_SYMBOL:
                self.x_wins += 1
            elif winner == COMPUTER_SYMBOL:
                self.o_wins += 1

            return

        if is_board_full(self.board):
            self.round_over = True
            self.winner = None

            # Task 2: update persistent scoreboard.
            self.draws += 1

    def draw(self, surface, font):
        from game import renderer

        renderer.draw_board(surface, self.board)

        turn_label = (
            "Your turn (X)"
            if self.current_player == HUMAN_SYMBOL
            else "Computer's turn (O)"
        )

        renderer.draw_text(surface, font, turn_label, (10, 10))

        # Persistent scoreboard.
        renderer.draw_scoreboard(
            surface,
            font,
            self.x_wins,
            self.o_wins,
            self.draws
        )

        # Task 4 controls.
        renderer.draw_controls(
            surface,
            font,
            self.starting_player
        )

        if self.round_over:
            text = f"{self.winner} wins!" if self.winner else "Draw!"

            renderer.draw_banner(
                surface,
                font,
                text
            )