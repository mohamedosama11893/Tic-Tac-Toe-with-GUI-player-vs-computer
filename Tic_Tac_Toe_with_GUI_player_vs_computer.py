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

