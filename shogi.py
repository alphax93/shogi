from typing import Dict

from piece import Pawn, Lance, Knight, SilverGeneral, GoldGeneral, King, Piece, \
    Rook, Bishop

import inquirer


class Board:
    def __init__(self):
        self._size = 9
        self._board = [self._row_of_king("w"),
                       self._row_of_rook_bishop("w"),
                       # self._row_of_pawns("w"),
                       ["", "", "", "", "", "", "", "", ""],
                       ["", "", "", "", "", "", "", "", ""],
                       ["", "", "", "", "", "", "", "", ""],
                       self._row_of_pawns("w"),
                       ["", "", "", "", "", "", "", "", ""],
                       ["", "", "", "", "", "", "", "", ""],
                       # self._row_of_pawns("b"),
                       # self._row_of_rook_bishop("b"),
                       self._row_of_king("b")
                       ]
        self._white_captured = []
        self._black_captured = []

    @staticmethod
    def _row_of_king(color):
        return [Lance(color), Knight(color), SilverGeneral(color),
                GoldGeneral(color), King(color), GoldGeneral(color),
                SilverGeneral(color), Knight(color), Lance(color)]

    @staticmethod
    def _row_of_rook_bishop(color):
        return ["", Rook(color), "", "", "", "", "", Bishop(color), ""]

    @staticmethod
    def _row_of_pawns(color):
        return [Pawn(color) for _ in range(0, 9)]

    def print_board(self):
        print(f"============White============")
        print(f"Captured: {self._white_captured}\n\n")

        print(f"  |  0   1   2   3   4   5   6   7   8")
        print(f"--+------------------------------------")

        for i, row in enumerate(self._board):
            print(f"{i} |", end=" ")
            for item in row:
                if isinstance(item, Piece):
                    print(item, end="  ")
                else:
                    print(f"   ", end=" ")
            print("")
        print(f"\n\nCaptured: {self._black_captured}")
        print(f"============Black============")

    def get_piece(self, row, col):
        return self._board[row][col]

    def clear_pos(self, row, col):
        self._board[row][col] = ""

    def move_piece(self, piece, row, col):
        if self._board[row][col] != "":
            if piece.color == "w":
                self._white_captured.append(self._board[row][col])
            else:
                self._black_captured.append(self._board[row][col])
        self._board[row][col] = piece

    def check_if_possible(self, options, color):
        result = []
        for option in options:
            if self._board[int(option[1])][int(option[4])] == "" or self._board[int(option[1])][int(option[4])].color != color:
                result.append(option)
        return result

    def check_direction(self, options, color):
        if isinstance(options, Dict):
            result = []
            for key in options.keys():
                if key != "others":
                    for option in options[key]:
                        if self._board[int(option[1])][int(option[4])] == "" or self._board[int(option[1])][int(option[4])].color != color:
                            result.append(option)
                        if self._board[int(option[1])][int(option[4])] != "":
                            break
            return result
        else:
            return options


b = Board()

turn = "w"
turn_count = 0

while True:
    b.print_board()
    print(f"\n\nTurn #{turn_count} {turn}")

    print("Which piece do you want to move? (row col)")
    x = int(input())
    y = int(input())

    try:
        selected_piece = b.get_piece(x, y)
        if selected_piece.color != turn:
            raise Exception("Select a piece of your color.")
        possible_moves = selected_piece.available_positions(x, y)
        if isinstance(selected_piece, Lance) or isinstance(selected_piece, Rook) or isinstance(selected_piece, Bishop):
            possible_moves = b.check_direction(possible_moves, selected_piece.color)

        possible_moves = b.check_if_possible(possible_moves, selected_piece.color)
        if not possible_moves:
            raise Exception("No moves available for this piece.")
        question = [inquirer.List("new_pos", "Where do you want to move it?",
                                  possible_moves)]
        answer = inquirer.prompt(question)["new_pos"]
        b.clear_pos(x, y)
        b.move_piece(selected_piece, int(answer[1]), int(answer[4]))

        if turn == "w" and int(answer[1]) >= 6 and not selected_piece.promoted:
            selected_piece.promote()
        if turn == "b" and int(answer[1]) <= 2 and not selected_piece.promoted:
            selected_piece.promote()

        turn = "w" if turn == "b" else "b"
        turn_count += 1

    except Exception as e:
        print(f"\033[91m{e}\033[00m")
        continue

