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
