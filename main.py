import src.ticdb as ticdb
import random
import src.ticboard as ticboard
from colorama import Fore

# Initialize database
cursor,db=ticdb.manage_db()

# Update scoreboard
def update_scoreboard(player_name):
    cursor.execute("INSERT INTO scores (player_name, wins) VALUES (%s, 1) "
                   "ON DUPLICATE KEY UPDATE wins = wins + 1", (player_name,))
    db.commit()

# Play a single round of Tic Tac Toe
def play_round():
    player_names = ['X', 'O']
    current_player = random.choice(player_names)
    board = ticboard.initialize_board()

    print(Fore.YELLOW + f"{current_player} goes first!")

    # Main game loop
    while True:
        ticboard.display_board(board)
        move = input(Fore.GREEN + f"\n{current_player}'s turn. Enter your move (0-8): ")

        if not move:
            print(Fore.RED + "Invalid input. Please enter a move (0-8).")
            continue

        try:
            move = int(move)
            if move < 0 or move > 8 or board[move] != ' ':
                raise ValueError("Invalid move.")
        except (ValueError, IndexError):
            print(Fore.RED + "Invalid move. Try again.")
            continue

        board[move] = 'X' if current_player == player_names[0] else 'O'

        if ticboard.check_winner(board, current_player):
            ticboard.display_board(board)
            if current_player == 'X':
                print(Fore.GREEN + f"{current_player} wins this round!")
                update_scoreboard(current_player)
            else:
                print(Fore.GREEN + f"{current_player} wins this round")
                update_scoreboard(current_player)
            break
        elif ' ' not in board:
            ticboard.display_board(board)
            print(Fore.GREEN + "It's a draw!")
            break

        current_player = player_names[0] if current_player == player_names[1] else player_names[1]

# Play the game with the specified number of rounds
def play_game(num_rounds):
    try:
        for _ in range(num_rounds):
            print(Fore.YELLOW + f"\nRound {_ + 1}:")
            play_round()

        # Display the final scoreboard and determine the winner
        print(Fore.YELLOW + "\nFinal Scoreboard:")
        cursor.execute("SELECT * FROM scores")
        scores = cursor.fetchall()
        winner = None
        winning_score = -1

        for score in scores:
            print(f"{score[0]}: {score[1]} wins")
            if score[1] > winning_score:
                winner = score[0]
                winning_score = score[1]
            elif score[1] == winning_score:
                winner = "It's a tie!"

        print(Fore.YELLOW + f"\nOverall Winner: {winner}")

    except KeyboardInterrupt:
        print("\nGame terminated.")
    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        db.close()

if __name__ == "__main__":
    try:
        num_rounds = int(input("Enter the number of rounds: "))
        play_game(num_rounds)
    except ValueError:
        print(Fore.RED + "Invalid input. Please enter a valid number of rounds.")

