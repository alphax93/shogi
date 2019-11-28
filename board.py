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
