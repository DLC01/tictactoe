from colorama import init, Fore, Style

# Initialize Colorama for colored output
init(autoreset=True)

# Initialize the Tic Tac Toe board
def initialize_board():
    board = [' ' for _ in range(9)]
    return board

# Display the Tic Tac Toe board with colors
def display_board(board):
    print(Fore.WHITE + ' ' + board[0] + ' | ' + board[1] + ' | ' + board[2])
    print('-----------')
    print(' ' + board[3] + ' | ' + board[4] + ' | ' + board[5])
    print('-----------')
    print(' ' + board[6] + ' | ' + board[7] + ' | ' + board[8])

# Check for a win condition
def check_winner(board, player):
    win_conditions = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                      (0, 3, 6), (1, 4, 7), (2, 5, 8),
                      (0, 4, 8), (2, 4, 6)]
    for condition in win_conditions:
        if all(board[i] == player for i in condition):
            return True
    return False

