import pygame
import sys
import time

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 400, 450
FPS = 60
LINE_WIDTH = 10
BOARD_ROWS, BOARD_COLS = 3, 3
PADDING = 20
SQUARE_SIZE = (WIDTH - 2 * PADDING) // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 5
CROSS_WIDTH = 15
SPACE = SQUARE_SIZE // 4
BUTTON_HEIGHT = 50
BUTTON_WIDTH = 100

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (67, 164, 175)
LINE_COLOR = (0, 0, 0)
CIRCLE_COLOR = (0, 0, 255)
CROSS_COLOR = (255, 0, 0)
TEXT_COLOR = (0, 0, 0)
BUTTON_COLOR = (26, 232, 177)
OVERLAY_COLOR = (0, 0, 0, 225)  # Semi-transparent black (RGBA)

# Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")
font = pygame.font.Font(None, 48)
screen.fill(WHITE)

# Board
board = ["-" for _ in range(9)]
player = "X"  # User is "X", AI is "O"

# Draw Grid
def draw_grid():
    # Horizontal Lines
    for row in range(1, BOARD_ROWS):
        pygame.draw.line(screen, LINE_COLOR, (PADDING, row * SQUARE_SIZE + PADDING), (WIDTH - PADDING, row * SQUARE_SIZE + PADDING), LINE_WIDTH)
    # Vertical Lines
    for col in range(1, BOARD_COLS):
        pygame.draw.line(screen, LINE_COLOR, (col * SQUARE_SIZE + PADDING, PADDING), (col * SQUARE_SIZE + PADDING, HEIGHT - BUTTON_HEIGHT - PADDING), LINE_WIDTH)

# Draw X and O  
def draw_markers():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            index = row * 3 + col
            x = col * SQUARE_SIZE + SQUARE_SIZE // 2 + PADDING
            y = row * SQUARE_SIZE + SQUARE_SIZE // 2 + PADDING

            if board[index] == "O":
                pygame.draw.circle(screen, CIRCLE_COLOR, (x, y), CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[index] == "X":
                pygame.draw.line(screen, CROSS_COLOR, (x - SPACE, y - SPACE), (x + SPACE, y + SPACE), CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR, (x - SPACE, y + SPACE), (x + SPACE, y - SPACE), CROSS_WIDTH)

# Check for a winner
def check_winner():
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]
    for combo in winning_combinations:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] and board[combo[0]] != "-":
            return board[combo[0]]
    return None

# Check for a draw
def check_draw():
    return "-" not in board

# Minimax Algorithm for AI
def minimax(board, depth, is_maximizing, alpha=-float('inf'), beta=float('inf')):
    winner = check_winner()
    if winner == "X":
        return -1
    elif winner == "O":
        return 1
    elif check_draw():
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for i in range(9):
            if board[i] == "-":
                board[i] = "O"
                score = minimax(board, depth + 1, False, alpha, beta)
                board[i] = "-"
                best_score = max(score, best_score)
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break
        return best_score
    else:
        best_score = float('inf')
        for i in range(9):
            if board[i] == "-":
                board[i] = "X"
                score = minimax(board, depth + 1, True, alpha, beta)
                board[i] = "-"
                best_score = min(score, best_score)
                beta = min(beta, best_score)
                if beta <= alpha:
                    break
        return best_score

# AI Move
def computer_move():
    best_score = -float('inf')
    best_move = None
    for i in range(9):
        if board[i] == "-":
            board[i] = "O"
            score = minimax(board, 0, False)
            board[i] = "-"
            if score > best_score:
                best_score = score
                best_move = i
    if best_move is not None:
        board[best_move] = "O"
    return best_move

# Reset Game
def reset_game():
    global board, player
    board = ["-" for _ in range(9)]
    player = "X"
    screen.fill(WHITE)
    draw_grid()
    show_overlay_text("Welcome to Tic Tac Toe", HEIGHT // 2 - 20, BLUE)

# Draw Text with Overlay
def show_overlay_text(message, y_offset, color):
    # Create a semi-transparent overlay
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill(OVERLAY_COLOR)
    screen.blit(overlay, (0, 0))

    # Draw the text
    text = font.render(message, True, color)
    text_rect = text.get_rect(center=(WIDTH // 2, y_offset))
    screen.blit(text, text_rect)

    pygame.display.update()
    time.sleep(3)  # Show the overlay and text for 3 seconds
    screen.fill(WHITE)  # Clear the screen
    draw_grid()  # BLUEraw the grid
    draw_reset_button()  # BLUEraw the reset button
    pygame.display.update()

# Draw Text
def draw_text(message, y_offset, color):
    text = font.render(message, True, color)
    text_rect = text.get_rect(center=(WIDTH // 2, y_offset))
    screen.blit(text, text_rect)

# Draw reset button
def draw_reset_button():
    button_rect = pygame.Rect(WIDTH // 4, HEIGHT - BUTTON_HEIGHT, WIDTH // 2, BUTTON_HEIGHT)
    pygame.draw.rect(screen, BUTTON_COLOR, button_rect)
    draw_text("Reset", HEIGHT - BUTTON_HEIGHT // 2, TEXT_COLOR)

# Initial screen setup
screen.fill(WHITE)
draw_grid()
show_overlay_text("Welcome to Tic Tac Toe", HEIGHT // 2 - 20, BLUE)

# Game loop
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos
            if HEIGHT - BUTTON_HEIGHT < y < HEIGHT:
                reset_game()
            else:
                row, col = (y - PADDING) // SQUARE_SIZE, (x - PADDING) // SQUARE_SIZE
                index = row * 3 + col
                if board[index] == "-":
                    board[index] = player  # User makes a move
                    winner = check_winner()
                    if winner:
                        show_overlay_text(f"Congratulations! {winner} Won", HEIGHT // 2 - 20, BLUE)
                        reset_game()
                    elif check_draw():
                        show_overlay_text("It's a Draw!", HEIGHT // 2 - 20, BLUE)
                        reset_game()
                    else:
                        # Switch to AI's turn
                        player = "O"
                        draw_markers()  # Update the screen to show the user's move
                        pygame.display.update()
                        time.sleep(1)  # Add a 1-second delay before the AI moves
                        ai_move = computer_move()  # AI makes a move
                        if ai_move is not None:
                            board[ai_move] = "O"
                            winner = check_winner()
                            if winner:
                                show_overlay_text(f"Congratulations! {winner} Won", HEIGHT // 2 - 20, BLUE)
                                reset_game()
                            elif check_draw():
                                show_overlay_text("It's a Draw!", HEIGHT // 2 - 20, BLUE)
                                reset_game()
                            else:
                                player = "X"  # Switch back to user's turn

    draw_markers()
    draw_reset_button()
    pygame.display.update()

pygame.quit()
sys.exit()