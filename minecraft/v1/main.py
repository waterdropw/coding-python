#!/bin/env python

import pygame
import sys
import random # Import random module
import os # Import the os module
from dataclasses import dataclass
from typing import Literal

@dataclass
class Cell:
    value: Literal['mine', 'empty', 'number']
    state: Literal['covered', 'revealed', 'flagged']


# Initialize Pygame
pygame.init()


# Screen dimensions
WIDTH, HEIGHT = 300, 300
CELL_SIZE = 30 # Example cell size

# Board dimensions and mines
ROWS = HEIGHT // CELL_SIZE
COLS = WIDTH // CELL_SIZE
NUM_MINES = 10 # Example number of mines

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (192, 192, 192)
DARK = (80, 80, 80)
LIGHT = (100, 100, 100)
RED = (255,0, 0)
GREEN = (0, 255, 0)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MineCraft")

# Get the directory of the current script
script_dir = os.path.dirname(__file__)
# Construct the full path to the mine image
mine_image_path = os.path.join(script_dir, 'mine.png')

# Load mine image
mine_image = pygame.image.load(mine_image_path)
mine_image = pygame.transform.scale(mine_image, (CELL_SIZE, CELL_SIZE))

# --- Game Variables ---
board = [] # Global variable to store the board state
game_state = 'playing' # 'playing', 'won', 'lost'
total_non_mines = 0 # To store the total number of non-mine cells

# --- Game Functions ---

def create_board():
    """Creates and initializes the game board."""
    global board, total_non_mines
    board = [[Cell('empty', 'covered') for _ in range(COLS)] for _ in range(ROWS)]
    total_cells = ROWS * COLS
    total_non_mines = total_cells - NUM_MINES

    # Place mines
    mines_placed = 0
    while mines_placed < NUM_MINES:
        row = random.randint(0, ROWS - 1)
        col = random.randint(0, COLS - 1)
        if board[row][col].value != 'mine':
            board[row][col].value = 'mine'
            mines_placed += 1

    # 如果当前格子不是雷，则需要计算它周围相邻9个位置总共有多少雷，并且显示出这个总数

    # Calculate numbers for non-mine cells
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c].value != 'mine':
                num_adjacent_mines = 0
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < ROWS and 0 <= nc < COLS and board[nr][nc].value == 'mine':
                            num_adjacent_mines += 1
                board[r][c].value = f'number_{num_adjacent_mines}'

def draw_board(screen):
    """Draws the current state of the game board."""
    for r in range(ROWS):
        for c in range(COLS):
            cell = board[r][c]
            x = c * CELL_SIZE
            y = r * CELL_SIZE
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)

            if cell.state == 'covered':
                # Draw base gray
                pygame.draw.rect(screen, GRAY, rect, 0)

                # Draw highlight (top and left)
                pygame.draw.line(screen, WHITE, (x, y), (x + CELL_SIZE - 1, y), 1)
                pygame.draw.line(screen, WHITE, (x, y), (x, y + CELL_SIZE - 1), 1)
                # Draw shadow (bottom and right)
                pygame.draw.line(screen, BLACK, (x + CELL_SIZE - 1, y), (x + CELL_SIZE - 1, y + CELL_SIZE - 1), 1)
                pygame.draw.line(screen, BLACK, (x, y + CELL_SIZE - 1), (x + CELL_SIZE - 1, y + CELL_SIZE - 1), 1)
            elif cell.state == 'revealed':
                # Draw base gray
                pygame.draw.rect(screen, LIGHT, rect, 0)
                # Draw base cell border
                pygame.draw.rect(screen, DARK, rect, 1)

                # Draw value if revealed
                if 'mine' in cell.value:
                    screen.blit(mine_image, rect.topleft)
                elif 'number' in cell.value:
                    num = int(cell.value.split('_')[1])
                    if num > 0: # Only draw numbers greater than 0
                        font = pygame.font.Font(None, 25)
                        text = font.render(str(num), True, BLACK) # You might want different colors for different numbers
                        text_rect = text.get_rect(center=rect.center)
                        screen.blit(text, text_rect)
                # If 'empty' and revealed, just draw the flat background
                elif 'empty' in cell.value:
                    # TODO: play a sound for good luck
                    pass
                else:
                    assert False
            
            # Draw cell border (optional, depends on desired look)
            # pygame.draw.rect(screen, BLACK, rect, 1)

            # TODO: Add drawing logic for flagged cells based on cell.state
            # if cell.state == 'flagged':
            #     # Draw flag icon
            #     pass

def handle_click(x, y, button):
    # Convert pixel coordinates to board coordinates
    col = x // CELL_SIZE
    row = y // CELL_SIZE

    # Check if the click is within the board boundaries
    if 0 <= row < ROWS and 0 <= col < COLS:
        cell = board[row][col]

        # Left click (button 1) to reveal
        if button == 1 and cell.state == 'covered':
            if cell.value == 'mine':
                cell.state = 'revealed' # Reveal the mine
                global game_state
                game_state = 'lost'
                print("Game Over! You hit a mine.") # Simple notification
            elif cell.value == 'number_0': # If it's an empty cell
                reveal_empty_cells(row, col)
                check_win_loss()
            elif 'number' in cell.value: # If it's a numbered cell (not 0)
                 cell.state = 'revealed'
                 check_win_loss()

        # Right click (button 3) to flag
        elif button == 3 and cell.state == 'covered':
            if cell.state == 'covered':
                cell.state = 'flagged'
            elif cell.state == 'flagged':
                cell.state = 'covered'

def reveal_empty_cells(row, col):
    """Recursively reveals empty cells and adjacent numbered cells."""
    # Check boundaries and if already revealed or flagged
    if not (0 <= row < ROWS and 0 <= col < COLS) or board[row][col].state != 'covered':
        return

    cell = board[row][col]
    cell.state = 'revealed'

    # If it's an empty cell (number_0), recursively reveal neighbors
    if cell.value == 'number_0':
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                reveal_empty_cells(row + dr, col + dc)

def check_win_loss():
    """Checks for win or loss conditions and updates game_state."""
    global game_state
    if game_state == 'lost': # If already lost, no need to check for win
        return

    revealed_non_mines = 0
    for r in range(ROWS):
        for c in range(COLS):
            cell = board[r][c]
            if cell.state == 'revealed' and cell.value != 'mine':
                revealed_non_mines += 1

    if revealed_non_mines == total_non_mines:
        game_state = 'won'
        print("Congratulations! You won!") # Simple notification

# --- Main Game Loop ---
def main():
    running = True
    create_board() # Call create_board to initialize the board

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN and game_state == 'playing': # Only handle clicks if game is playing
                x, y = event.pos
                handle_click(x, y, event.button)

        # --- Drawing ---
        screen.fill(WHITE) # Fill background
        draw_board(screen)
        
        # Display game state message
        if game_state != 'playing':
            font = pygame.font.Font(None, 50)
            message = "You Win!" if game_state == 'won' else "Game Over!"
            color = GREEN if game_state == 'won' else RED
            text = font.render(message, True, color)
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(text, text_rect)

        # --- Update Display ---
        pygame.display.flip() # Or pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
