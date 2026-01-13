import tkinter as tk
import random
import glob
from PIL import Image, ImageTk
import os

# ================================================================
# WORKFLOW (high-level)
# 1) Program starts and builds a Tk window.
# 2) Images for X and O are located under assets/characters/ using glob.
# 3) Images are loaded and converted to PhotoImage objects for Tkinter.
# 4) Top frame shows the score, turn label and result text; a restart button calls start_new_game().
# 5) Bottom frame builds a 3x3 grid of Buttons stored in cell_buttons.
# 6) When the player clicks a cell -> next_turn(row, col) executes:
#      - place player's symbol (image + text) if it's the player's turn and the cell is empty
#      - check for a winner or tie
#      - if the game continues, switch to computer turn and call computer_move() after a short delay
# 7) computer_move() picks a random empty cell, places the computer symbol, then checks for win/tie.
# 8) handle_game_end() and handle_tie() set game_over, update result_text and scores.
# 9) start_new_game() clears the board, chooses starter and symbols randomly and may start the computer.
# ================================================================

def load_game_assets(category):
    """
    Search assets/<category>/ for PNG files and return a dict with keys "X" and "O".
    Heuristics:
      - If filename contains 'x' (and not 'o') assign as X.
      - If filename contains 'o' (and not 'x') assign as O.
    Falls back to remaining files if explicit names are not found.
    """
    pattern = os.path.join("assets", category, "*.png")
    files = glob.glob(pattern)
    assets = {}
    for file in files:
        name = os.path.splitext(os.path.basename(file))[0].lower()
        if "x" in name and "o" not in name:
            assets["X"] = file
        elif "o" in name and "x" not in name:
            assets["O"] = file
    # fallback: if explicit names are not found, take remaining files (first -> X, second -> O)
    remaining = [f for f in files if f not in (assets.get("X"), assets.get("O"))]
    if "X" not in assets and remaining:
        assets["X"] = remaining.pop(0)
    if "O" not in assets and remaining:
        assets["O"] = remaining.pop(0)
    return assets


# Game control variables
player_symbol = "X"
comp_symbol = "O"
current_turn = "player"   # either 'player' or 'computer'
game_over = False

def next_turn(row, col):
    """
    Handle a player's click on cell (row, col).
    - Only accept clicks when it's player's turn and the game is not over.
    - Place player's symbol (image + text).
    - Check for a win or tie; if neither, switch to computer and schedule computer_move().
    """
    global current_turn, game_over
    # ignore click if it's not the player's turn or the game has ended
    if current_turn != "player" or game_over:
        return
    # ignore click if the cell is not empty
    if cell_buttons[row][col]['text'] != "":
        return

    # place player's symbol (image + text)
    sym = player_symbol
    img = x_img if sym == "X" else o_img
    cell_buttons[row][col].config(image=img, text=sym)

    # check for win or tie
    winner = check_win()
    if winner:
        handle_game_end(winner)
        return
    if not check_empty_spaces():
        handle_tie()
        return

    # switch to computer turn and schedule computer move after a short delay
    current_turn = "computer"
    update_turn_label()
    window.after(2000, computer_move)

def check_win():
    """
    Check all possible winning lines (rows, columns, diagonals).
    If a winning line is found, color the three cells and return the winning symbol 'X' or 'O'.
    Otherwise return False.
    """
    lines = [
        [(0, 0), (0, 1), (0, 2)], [(1, 0), (1, 1), (1, 2)], [(2, 0), (2, 1), (2, 2)],
        [(0, 0), (1, 0), (2, 0)], [(0, 1), (1, 1), (2, 1)], [(0, 2), (1, 2), (2, 2)],
        [(0, 0), (1, 1), (2, 2)], [(0, 2), (1, 1), (2, 0)]
    ]
    for line in lines:
        a, b, c = line
        ta = cell_buttons[a[0]][a[1]]['text']
        tb = cell_buttons[b[0]][b[1]]['text']
        tc = cell_buttons[c[0]][c[1]]['text']
        if ta != "" and ta == tb == tc:
            # color winning cells
            cell_buttons[a[0]][a[1]].config(bg='#23F0F0')
            cell_buttons[b[0]][b[1]].config(bg='#23F0F0')
            cell_buttons[c[0]][c[1]].config(bg='#23F0F0')
            return ta
    return False


def check_empty_spaces():
    """
    Return True if there is at least one empty cell (text == ""), otherwise False.
    """
    for r in range(3):
        for c in range(3):
            if cell_buttons[r][c]['text'] == "":
                return True
    return False

def computer_move():
    """
    Computer picks a random empty cell and places its symbol.
    After the move, check for a win or tie and switch back to player if the game continues.
    """
    global current_turn, game_over
    if game_over:
        return
    empty_cells = [(r, c) for r in range(3) for c in range(3) if cell_buttons[r][c]['text'] == ""]
    if not empty_cells:
        return
    r, c = random.choice(empty_cells)
    sym = comp_symbol
    img = x_img if sym == "X" else o_img
    cell_buttons[r][c].config(image=img, text=sym)

    winner = check_win()
    if winner:
        handle_game_end(winner)
        return
    if not check_empty_spaces():
        handle_tie()
        return

    # switch back to player
    current_turn = "player"
    update_turn_label()

def handle_game_end(winner_symbol):
    """
    Handle the end of the game when a winner is detected.
    - Set game_over flag.
    - Update result_text and increment the correct score.
    - Refresh the displayed score.
    """
    global game_over
    game_over = True
    if winner_symbol == player_symbol:
        result_text.set("You Win!")
        user_score.set(user_score.get() + 1)
    else:
        result_text.set("Computer Wins!")
        computer_score.set(computer_score.get() + 1)
    update_score_text()
    
def handle_tie():
    """
    Handle a tie (no empty spaces and no winner).
    - Set game_over flag.
    - Set result_text to "Tie!" and color cells as a visual cue.
    """
    global game_over
    game_over = True
    result_text.set("Tie!")
    # color cells as a tie indicator
    for r in range(3):
        for c in range(3):
            if cell_buttons[r][c]['text'] != "":
                cell_buttons[r][c].config(bg='red')
                
def update_score_text():
    """Update the score label text variable from the current IntVar values."""
    score_text.set(f"You: {user_score.get()}   Computer: {computer_score.get()}")


def update_turn_label():
    """Update the turn label showing who is to move and which symbol they use."""
    if current_turn == "player":
        player_label.config(text=f"Player Turn: Player ({player_symbol})")
    else:
        player_label.config(text=f"Player Turn: Computer ({comp_symbol})")


# ---------------- GUI ----------------
window = tk.Tk()
window.title("X O Game by Mohamed Osama")
window.geometry("420x700")
window.resizable(False, False)

# load images (after root window is created)
assets = load_game_assets("characters")
if not assets.get("X") or not assets.get("O"):
    raise RuntimeError("Missing images!")

x_img = ImageTk.PhotoImage(Image.open(assets["X"]).resize((100, 100)))
o_img = ImageTk.PhotoImage(Image.open(assets["O"]).resize((100, 100)))

# UI variables
user_score = tk.IntVar(value=0)
computer_score = tk.IntVar(value=0)
result_text = tk.StringVar(value="")
score_text = tk.StringVar(value=f"You: {user_score.get()}   Computer: {computer_score.get()}")

# ---- top frame ----
top_frame = tk.Frame(window)
top_frame.pack(pady=12)

score_label = tk.Label(top_frame, textvariable=score_text, font=("Arial", 16, "bold"))
score_label.pack()

player_label = tk.Label(top_frame, text="", font=("Arial", 16))
player_label.pack(pady=6)

winner_label = tk.Label(top_frame, textvariable=result_text, font=("Arial", 18, "bold"))
winner_label.pack(pady=6)

restart_button = tk.Button(top_frame, text="Start / Restart", font=("Arial", 14), command=start_new_game)
restart_button.pack(pady=6)

# ---- bottom frame (game board) ----
bottom_frame = tk.Frame(window)
bottom_frame.pack(expand=True, fill="both", padx=12, pady=12)

# buttons matrix
cell_buttons = [[None] * 3 for _ in range(3)]
for ro in range(3):
    bottom_frame.rowconfigure(ro, weight=1, minsize=120)
    for co in range(3):
        bottom_frame.columnconfigure(co, weight=1, minsize=120)
        btn = tk.Button(bottom_frame, text="", font=("Arial", 36, "bold"),
                        command=lambda rr=ro, cc=co: next_turn(rr, cc))
        btn.grid(row=ro, column=co, sticky="nsew", padx=4, pady=4)
        cell_buttons[ro][co] = btn

# start the first game
start_new_game()

window.mainloop()
