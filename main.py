import mysql.connector
import sys
import random
from colorama import init, Fore, Style

# Initialize colorama for colored output
init(autoreset=True)

# Connect to MySQL database
try:
    db = mysql.connector.connect(
        user="<username>",
        password="<password>",
        host="localhost",
        database="tictactoe"

    )
except mysql.connector.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Get Cursor
cursor = db.cursor()

#create table if it doesnt exist
create_table_sql = """
CREATE TABLE IF NOT EXISTS tic_tac_toe_scores (
    player_name VARCHAR(255) PRIMARY KEY,
    wins INT
)
"""
cursor.execute(create_table_sql)
db.commit()

# Initialize the Tic Tac Toe board
board = [' ' for _ in range(9)]

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

# Update scoreboard
def update_scoreboard(player_name):
    cursor.execute("INSERT INTO scores (player_name, wins) VALUES (%s, 1) "
                   "ON DUPLICATE KEY UPDATE wins = wins + 1", (player_name,))
    db.commit()

# AI makes a random move
def ai_move():
    return random.choice([i for i, x in enumerate(board) if x == ' '])

# Main game loop
def main():
    print(Fore.YELLOW + "Welcome to Tic Tac Toe!")
    player_name = input("Enter your name: ")
    current_player = random.choice(['X', 'O'])
    is_ai_turn = False

    while True:
        print(Fore.CYAN + "\nCurrent Board:")
        display_board(board)
        
        if current_player == 'X':
            move = int(input(Fore.GREEN + f"\n{current_player}'s turn. Enter your move (0-8): "))
        else:
            print(Fore.GREEN + f"\n{current_player} (AI)'s turn.")
            move = ai_move()

        if board[move] == ' ':
            board[move] = current_player
            if check_winner(board, current_player):
                print(Fore.CYAN + "\nUpdated Board:")
                display_board(board)
                if current_player == 'X':
                    print(Fore.GREEN + f"\n{current_player} wins!")
                    update_scoreboard(player_name)
                else:
                    print(Fore.GREEN + f"\n{current_player} (AI) wins!")
                break
            elif ' ' not in board:
                print(Fore.CYAN + "\nUpdated Board:")
                display_board(board)
                print(Fore.GREEN + "\nIt's a draw!")
                break
            current_player = 'O' if current_player == 'X' else 'X'
        else:
            print(Fore.RED + "\nInvalid move. Try again.")

    db.close()

if __name__ == "__main__":
    main()

