from abc import abstractmethod


class Piece:

    def __init__(self, icon, color):
        self._icon = icon
        self._color = color
        self.promoted = False

    def __repr__(self):
        return f"{self._icon}{self._color}"

    @abstractmethod
    def available_positions(self, row, col):
        pass

    @abstractmethod
    def promote(self):
        pass

    @abstractmethod
    def unpromote(self):
        pass

    @property
    def color(self):
        return self._color

    @property
    def icon(self):
        return self._icon

    @icon.setter
    def icon(self, new_icon):
        self._icon = new_icon

    def change_color(self):
        self._color = "w" if self._color == "b" else "b"


class Pawn(Piece):
    def __init__(self, color):
        super().__init__("P", color)

    def available_positions(self, row, col):
        if not self.promoted:
            if self._color == "w":
                return [f"({row + 1}, {col})"]
            else:
                return [f"({row - 1}, {col})"]
        else:
            return _gold_move(row, col, self.color)

    def promote(self):
        self.promoted = True
        self.icon = "+P"

    def unpromote(self):
        self.promoted = False
        self.icon = "P"


class King(Piece):
    def __init__(self, color):
        super().__init__("K", color)

    def available_positions(self, row, col):
        result = [f"({row - 1}, {col - 1})",
                  f"({row - 1}, {col})",
                  f"({row - 1}, {col + 1})",
                  f"({row}, {col - 1})",
                  f"({row}, {col + 1})",
                  f"({row + 1}, {col - 1})",
                  f"({row + 1}, {col})",
                  f"({row + 1}, {col + 1})"]

        return [pos for pos in result if "-" not in pos and "9" not in pos]

    def promote(self):
        pass

    def unpromote(self):
        pass


class Rook(Piece):
    def __init__(self, color):
        super().__init__("R", color)

    def available_positions(self, row, col):
        result = {"up": [f"({i}, {col})" for i in range(0, row)],
                "down": [f"({i}, {col})" for i in range(row + 1, 9)],
                "left": [f"({row}, {i})" for i in range(0, row)],
                "right": [f"({row}, {i})" for i in range(col + 1, 9)]}

        if self.promoted:
            result["others"] = [f"({row - 1}, {col - 1})",
                                f"({row - 1}, {col + 1})",
                                f"({row + 1}, {col - 1})",
                                f"({row + 1}, {col + 1})"]

        return result

    def promote(self):
        self.promoted = True
        self.icon = "+R"

    def unpromote(self):
        self.promoted = False
        self.icon = "R"


class Bishop(Piece):
    def __init__(self, color):
        super().__init__("B", color)

    def available_positions(self, row, col):
        result = {"up": [f"({i}, {j})" for i, j in zip(range(row - 1, -1, -1), range(col - 1, -1, -1))],  # up-left
                "down": [f"({i}, {j})" for i, j in zip(range(row + 1, 9), range(col + 1, 9))],  # down-right
                "left": [f"({i}, {j})" for i, j in zip(range(row + 1, 9), range(col - 1, -1, -1))],  # down-left
                "right": [f"({i}, {j})" for i, j in zip(range(row - 1, -1, -1), range(col + 1, 9))]}  # up-right

        if self.promoted:
            result["others"] = [f"({row - 1}, {col})",
                                f"({row}, {col - 1})",
                                f"({row}, {col + 1})",
                                f"({row + 1}, {col})"]

        return result

    def promote(self):
        self.promoted = True
        self.icon = "+B"

    def unpromote(self):
        self.promoted = False
        self.icon = "B"


class GoldGeneral(Piece):
    def __init__(self, color):
        super().__init__("G", color)

    def available_positions(self, row, col):
        return _gold_move(row, col, self.color)

    def promote(self):
        pass

    def unpromote(self):
        pass


class SilverGeneral(Piece):
    def __init__(self, color):
        super().__init__("S", color)

    def available_positions(self, row, col):
        if not self.promoted:
            if self.color == "w":
                result = [f"({row - 1}, {col - 1})",
                          f"({row - 1}, {col + 1})",
                          f"({row + 1}, {col - 1})",
                          f"({row + 1}, {col})",
                          f"({row + 1}, {col + 1})"]
            else:
                result = [f"({row - 1}, {col - 1})",
                          f"({row - 1}, {col})",
                          f"({row - 1}, {col + 1})",
                          f"({row + 1}, {col - 1})",
                          f"({row + 1}, {col + 1})"]

            return [pos for pos in result if "-" not in pos and "9" not in pos]
        else:
            return _gold_move(row, col, self.color)

    def promote(self):
        self.promoted = True
        self.icon = "+S"

    def unpromote(self):
        self.promoted = False
        self.icon = "S"


class Knight(Piece):
    def __init__(self, color):
        super().__init__("N", color)

    def available_positions(self, row, col):
        if not self.promoted:
            if self.color == "w":
                result = [f"({row + 2}, {col - 1})",
                          f"({row + 2}, {col + 1})"]
            else:
                result = [f"({row - 2}, {col - 1})",
                          f"({row - 2}, {col + 1})"]

            return [pos for pos in result if "-" not in pos and "9" not in pos]
        else:
            return _gold_move(row, col, self.color)

    def promote(self):
        self.promoted = True
        self.icon = "+N"

    def unpromote(self):
        self.promoted = False
        self.icon = "N"


class Lance(Piece):
    def __init__(self, color):
        super().__init__("L", color)

    def available_positions(self, row, col):
        if not self.promoted:
            if self.color == "w":
                return {"down": [f"({i}, {col})" for i in range(row+1, 9)]}
            else:
                return {"up": [f"({i}, {col})" for i in range(row-1, -1, -1)]}
        else:
            return _gold_move(row, col, self.color)

    def promote(self):
        self.promoted = True
        self.icon = "+L"

    def unpromote(self):
        self.promoted = False
        self.icon = "L"


def _gold_move(row, col, color):
    if color == "w":
        result = [f"({row - 1}, {col})",
                  f"({row}, {col - 1})",
                  f"({row}, {col + 1})",
                  f"({row + 1}, {col - 1})",
                  f"({row + 1}, {col})",
                  f"({row + 1}, {col + 1})"]
    else:
        result = [f"({row - 1}, {col - 1})",
                  f"({row - 1}, {col})",
                  f"({row - 1}, {col + 1})",
                  f"({row}, {col - 1})",
                  f"({row}, {col + 1})",
                  f"({row + 1}, {col})"]

    return [pos
            for pos in result if "-" not in pos and "9" not in pos]