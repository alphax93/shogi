from typing import Dict

from board import Board

from piece import Lance, Rook, Bishop

import inquirer


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
        question = [inquirer.List("new_pos", "Where do you want to move it? (row, col)",
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

