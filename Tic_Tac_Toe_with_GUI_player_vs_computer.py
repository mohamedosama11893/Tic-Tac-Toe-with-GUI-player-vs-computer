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