from typing import Dict

from piece import Pawn, Lance, Knight, SilverGeneral, GoldGeneral, King, Piece, \
    Rook, Bishop


class Board:
    def __init__(self):
        self._size = 9
        self._board = [self._row_of_king("w"),
                       self._row_of_rook_bishop("w"),
                       self._row_of_pawns("w"),
                       ["", "", "", "", "", "", "", "", ""],
                       ["", "", "", "", "", "", "", "", ""],
                       ["", "", "", "", "", "", "", "", ""],
                       self._row_of_pawns("b"),
                       self._row_of_rook_bishop("b"),
                       self._row_of_king("b")
                       ]
        self._white_captured = []
        self._black_captured = []
        self._free_places = ["(1, 0)", "(1, 2)", "(1, 3)", "(1, 4)", "(1, 5)", "(1, 6)", "(1, 8)"]

        for i in range(3, 6):
            for j in range(0, 9):
                self._free_places.append(f"({i}, {j})")
        self._free_places.extend(["(7, 0)", "(7, 2)", "(7, 3)", "(7, 4)", "(7, 5)", "(7, 6)", "(7, 8)"])
        self._free_places.sort()

    @property
    def white_captured(self):
        return self._white_captured

    @property
    def black_captured(self):
        return self._black_captured

    @property
    def free_places(self):
        return self._free_places

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
        self._free_places.append(f"({row}, {col})")
        self._free_places.sort()

    def move_piece(self, piece, row, col):
        if self._board[row][col] != "":
            if piece.color == "w":
                self._white_captured.append(self._board[row][col])
            else:
                self._black_captured.append(self._board[row][col])
        self._board[row][col] = piece
        try:
            self._free_places.remove(f"({row}, {col})")
        except:
            pass
        self._free_places.sort()

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

    def place_piece(self, piece, row, col):
        piece.unpromote()
        self._board[row][col] = piece
        self.free_places.remove(f"({row}, {col})")

    def check_if_can_place(self, piece):
        options = self.free_places.copy()

        if piece.icon == "N" or piece.icon == "P" or piece.icon == "L":
            if piece.color == "w":
                for j in range(0, 9):
                    if f"(8, {j})" in options:
                        options.remove(f"(8, {j})")
            else:
                for j in range(0, 9):
                    if f"(0, {j})" in options:
                        options.remove(f"(0, {j})")

        if piece.icon == "N":
            if piece.color == "w":
                for j in range(0, 9):
                    if f"(7, {j})" in options:
                        options.remove(f"(7, {j})")
            else:
                for j in range(0, 9):
                    if f"(1, {j})" in options:
                        options.remove(f"(1, {j})")

        if piece.icon == "P":
            cols_to_elim = []
            for j in range(0, 9):
                for i in range(0, 9):

                    if isinstance(self._board[i][j], Pawn) and self._board[i][j].icon == "P" and self._board[i][j].color == piece.color:
                        cols_to_elim.append(j)
                        break

            for j in cols_to_elim:
                for i in range(0, 9):
                    if f"({i}, {j})" in options:
                        options.remove(f"({i}, {j})")

        return options
