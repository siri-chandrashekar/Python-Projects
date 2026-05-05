board = [" " for _ in range(9)]


# ---------------- RESET BOARD ----------------
def reset_board():
    for i in range(9):
        board[i] = " "


# ---------------- PRINT BOARD ----------------
def print_board():
    print("\n")
    print(f"{board[0]} | {board[1]} | {board[2]}")
    print("--+---+--")
    print(f"{board[3]} | {board[4]} | {board[5]}")
    print("--+---+--")
    print(f"{board[6]} | {board[7]} | {board[8]}")
    print("\n")


# ---------------- CHECK WINNER ----------------
def check_winner(player):
    win_positions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
        [0, 4, 8], [2, 4, 6]              # diagonals
    ]
    for pos in win_positions:
        if board[pos[0]] == board[pos[1]] == board[pos[2]] == player:
            return True
    return False


# ---------------- DRAW CHECK ----------------
def is_draw():
    return " " not in board


# ---------------- MINIMAX AI ----------------
def minimax(is_maximizing):
    if check_winner("O"):
        return 1
    if check_winner("X"):
        return -1
    if is_draw():
        return 0

    if is_maximizing:
        best_score = -100
        for i in range(9):
            if board[i] == " ":
                board[i] = "O"
                score = minimax(False)
                board[i] = " "
                best_score = max(score, best_score)
        return best_score

    best_score = 100
    for i in range(9):
        if board[i] == " ":
            board[i] = "X"
            score = minimax(True)
            board[i] = " "
            best_score = min(score, best_score)
    return best_score


# ---------------- COMPUTER MOVE ----------------
def computer_move():
    best_score = -100
    move = None

    for i in range(9):
        if board[i] == " ":
            board[i] = "O"
            score = minimax(False)
            board[i] = " "

            if score > best_score:
                best_score = score
                move = i

    return move


# ---------------- PLAYER INPUT ----------------
def player_move():
    while True:
        try:
            move = int(input("Choose position (1-9): ")) - 1
            if move not in range(9):
                print("Invalid position. Try 1-9.")
            elif board[move] != " ":
                print("Position already taken.")
            else:
                return move
        except ValueError:
            print("Enter a number between 1 and 9.")


# ---------------- REPLAY PROMPT ----------------
def ask_play_again():
    while True:
        choice = input("Play another game? (yes/no): ").strip().lower()
        if choice in ("yes", "y"):
            return True
        if choice in ("no", "n"):
            return False
        print("Please type yes or no.")


# ---------------- SINGLE GAME LOOP ----------------
def play_round():
    reset_board()

    while True:
        print_board()

        # PLAYER TURN
        move = player_move()
        board[move] = "X"

        if check_winner("X"):
            print_board()
            print("You win!")
            break

        if is_draw():
            print_board()
            print("It's a draw!")
            break

        # COMPUTER TURN
        print("Computer thinking...")
        move = computer_move()
        board[move] = "O"

        if check_winner("O"):
            print_board()
            print("Computer wins!")
            break

        if is_draw():
            print_board()
            print("It's a draw!")
            break


# ---------------- GAME LOOP ----------------
def play_game():
    print("TIC TAC TOE")
    print("You = X | Computer = O")
    print("Positions are numbered 1-9 left to right.\n")

    while True:
        play_round()
        if not ask_play_again():
            print("Thanks for playing!")
            break


# ---------------- RUN ----------------
if __name__ == "__main__":
    play_game()
