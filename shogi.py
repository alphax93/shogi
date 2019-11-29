from board import Board

from piece import Lance, Rook, Bishop

import inquirer


b = Board()

turn = "w"
turn_count = 0

while True:
    b.print_board()
    print(f"\n\nTurn #{turn_count} {turn}")

    question = [
        inquirer.List("action", "What do you want to do?",
                      ["Move a piece", "Place a captured piece"])]
    answer = inquirer.prompt(question)["action"]

    if answer == "Move a piece":

        print("Which piece do you want to move? (press '9' to cancel)")
        x = int(input("Row: "))
        if x == 9:
            continue
        y = int(input("Col: "))
        if y == 9:
            continue

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

            if turn == "w" and not selected_piece.promoted:
                if ((selected_piece.icon == "P" or selected_piece.icon == "L") and int(answer[1]) == 8) or (selected_piece.icon == "N" and int(answer[1]) >= 7):
                    selected_piece.promote()
                elif int(answer[1]) >= 6:
                    question = [inquirer.List("promote",
                                              f"Do you want to promote {selected_piece}",
                                              ["Yes", "No"])]
                    answer = inquirer.prompt(question)["promote"]
                    if answer == "Yes":
                        selected_piece.promote()

            elif turn == "b" and not selected_piece.promoted:
                if ((selected_piece.icon == "P" or selected_piece.icon == "L") and int(answer[1]) == 0) or (selected_piece.icon == "N" and int(answer[1]) <= 1):
                    selected_piece.promote()
                elif int(answer[1]) >= 2:
                    question = [inquirer.List("promote",
                                              f"Do you want to promote {selected_piece}",
                                              ["Yes", "No"])]
                    answer = inquirer.prompt(question)["promote"]
                    if answer == "Yes":
                        selected_piece.promote()

        except Exception as e:
            print(f"\033[91m{e}\033[00m")
            continue

    else:
        options = []
        if turn == "w":
            options = b.white_captured.copy()
        else:
            options = b.black_captured.copy()

        options.append("Cancel")

        question = [inquirer.List("selected_piece",
                                  "Which piece do you want to place?",
                                  options)]
        selected_piece = inquirer.prompt(question)["selected_piece"]

        if isinstance(selected_piece, str):
            continue
        selected_piece.change_color()
        options = b.check_if_can_place(selected_piece)
        options.append("Cancel")
        question = [inquirer.List("place",
                                  "Where do you want to put it?",
                                  options)]
        place = inquirer.prompt(question)["place"]
        if isinstance(place, str):
            continue
        b.place_piece(selected_piece, int(place[1]), int(place[4]))

        if turn == "w":
            b.white_captured.remove(selected_piece)
        else:
            b.black_captured.remove(selected_piece)

    turn = "w" if turn == "b" else "b"
    turn_count += 1