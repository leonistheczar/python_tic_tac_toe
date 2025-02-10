# Tic Tac Game Console Based Game (User vs Computer)
import random
# Welcome
print("-------------------------------------------")
print("Welcome to Tic Tac Toe Game")
print("-------------------------------------------")

# Board Representation
board = ["-" for i in range(9)]     # List creation for board
# Print Board
def generate_board(board):
    print(f"{board[0]} | {board[1]} | {board[2]}")
    print("--+---+--")
    print(f"{board[3]} | {board[4]} | {board[5]}")
    print("--+---+--") 
    print(f"{board[6]} | {board[7]} | {board[8]}")

# Player Turns
def player_move(player, position):
    if board[position] == "-" :      # Checks for valid place 
        board[position] = player
        return True
    else:
        return False

# Checks for draw
def check_draw(board):
    if "-" not in board:
        return True
    else:
        return False
# Switch player after each turn
def switch_player(player):
    if player == "X":
        return "O"
    else: 
        return "X"
def check_winner(board):
    winning_combo = [[0,1,2], [3,4,5], [6,7,8],
                     [0,3,6], [1,4,7], [2,5,8],
                     [0,4,8], [2,4,6]]
    for combos in winning_combo:
        if board[combos[0]] == board[combos[1]] == board[combos[2]] != "-":
            return board[combos[0]]
    return None

# User move
def user_input(player):
    while True:
            position = (input(f"Enter position between 0-8 , {player} turn : "))
            if position == "":
                print("Invalid move. Try again")
                generate_board(board)
                continue
            try:
                position = int(position) 
                if position == -1:
                    return -1
                elif position < 0 or position > 8:
                    print("Invalid move. Please choose a number between 0-8.")
                    generate_board(board)
                elif board[position] != "-":
                    print("Invalid move. That position is already taken.")
                else:
                    return position  # Switch player
            except ValueError:
                print("Invalid move. Try again")

# Minimax Algorithm to evaluate the best move for the computer
def minimax(board, depth, is_maximizing, alpha = -float('inf'), beta = float('inf')):
    winner = check_winner(board)
    if winner == "X":
        return -1  
    elif winner == "O":
        return 1  
    elif check_draw(board):
        return 0  
    
    # If it's AI's turn (maximize score)
    if is_maximizing:
        best_score = -float('inf')  #  lowest possible score
        for i in range(9):
            if board[i] == "-":  
                board[i] = "O"  
                score = minimax(board, depth + 1, False, alpha, beta)  # Minimize for the opponent
                board[i] = "-"  
                best_score = max(score, best_score) 
                alpha = max(alpha, best_score)  # Update beta
                if beta <= alpha:  # Alpha cutoff
                    break
        return best_score
    else:  
        best_score = float('inf')  # highest possible score
        for i in range(9):
            if board[i] == "-":   
                board[i] = "X"  
                score = minimax(board, depth + 1, True, alpha, beta)  # Maximize for the AI
                board[i] = "-"  
                best_score = min(score, best_score)  
                beta = min(beta, best_score)  # Update beta
                if beta <= alpha:  # Alpha cutoff
                    break   
        return best_score
    
def computer_input():
    best_score = -float('inf')  # Start with the lowest possible score
    best_move = None
    
    for i in range(9):
        if board[i] == "-": 
            board[i] = "O"  
            score = minimax(board, 0, False)  
            board[i] = "-"  
            if score > best_score:  
                best_score = score
                best_move = i
    return best_move  
        
def play_game():
    player = "X"   # Player X starts the game
    while True:
        generate_board(board)

        if player == "X":
            position = user_input(player)
            if position == -1:
                print("Game exits!!!")
                break
        else:
            print("Computer's turn")
            position = computer_input()

        if player_move(player, position):
            winner = check_winner(board)
            if winner:
                generate_board(board)
                print(f"Congratulations!!! {winner} has won the game")
                break
            elif check_draw(board):
                print("It's a draw")
                break
            player = switch_player(player)
        else:
            print("Invalid move. Try again!!!")
#  Start
if __name__ == "__main__":
    play_game()