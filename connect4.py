import numpy as np
import random

# matrix to represent the Connect4 grid
x = 6
y = 7
grid = np.zeros((x,y))
print(grid)

# Drop a piece onto the grid based a selected column
def move(grid,col,piece):
    for r in range(x-1,-1,-1):
        if grid[r][col] == 0:
            grid[r][col] = piece
            break

# Returns True when connect4 is obtained
def connect4(grid, player):
    # Check for horizonal connect4
    for c in range(y-3):
        for r in range(x):
            if grid[r][c] == player and grid[r][c+1] == player and grid[r][c+2] == player and grid[r][c+3] == player:
                return True

    # Check for verticle connect4
    for c in range(y):
        for r in range(x-3):
            if grid[r][c] == player and grid[r+1][c] == player and grid[r+2][c] == player and grid[r+3][c] == player:
                return True

    # Check positive diagonal connect4
    for c in range(y-3):
        for r in range(x-3):
            if grid[r][c] == player and grid[r+1][c+1] == player and grid[r+2][c+2] == player and grid[r+3][c+3] == player:
                return True

    # Check negative diagonal connect4
    for c in range(y-3):
        for r in range(3,x):
            if grid[r][c] == player and grid[r-1][c+1] == player and grid[r-2][c+2] == player and grid[r-3][c+3] == player:
                return True

# Evaluate the grid and assign an effectiveness score to help in picking the right move
def evalute_grid(grid):
    effectiveness = 0

    def score(block):
        score = 0
    
        if block.count(2) == 4:
            score += 150
        elif block.count(2) == 3 and block.count(0) == 1:
            score += 20
        elif block.count(2) == 2 and block.count(0) == 2:
            score += 10
        
        # Reduce score if it gives player 1 a chance to win
        if block.count(1) == 3 and block.count(0) == 1:
            score -= 10

        return score

    # Evaluate horizontal blocks
    for r in range(x):
        for c in range(y-3):
            block = [grid[r][c],grid[r][c+1],grid[r][c+2],grid[r][c+3]]
            effectiveness += score(block)
    
    # Evaluate verticle blocks
    for r in range(x-3):
        for c in range(y):
            block = [grid[r][c],grid[r+1][c],grid[r+2][c],grid[r+3][c]]
            effectiveness += score(block)

    # Evaluate positive diagonal blocks
    for r in range(x-3):
        for c in range(y-3):
            block = [grid[r][c],grid[r+1][c+1],grid[r+2][c+2],grid[r+3][c+3]]
            effectiveness += score(block)

    # Evaluate negative diagonal blocks
    for r in range(3,x):
        for c in range(y-3):
            block = [grid[r][c],grid[r-1][c+1],grid[r-2][c+2],grid[r-3][c+3]]
            effectiveness += score(block)
    
    return effectiveness

# https://en.wikipedia.org/wiki/Minimax#Pseudocode
# https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning#Pseudocode
def minimax(grid, depth, alpha, beta, maximizingPlayer):
    # Array of available options of where to play
    options = []
    for c in range(y):
        if grid[0][c] == 0:
            options.append(c)  

    # Connect 4 is terminal when either player has connect4 or there are no more moves (a draw)
    terminal = connect4(grid, 1) or connect4(grid, 2) or len(options) == 0
    if depth == 0 or terminal:
        if terminal:
            if connect4(grid, 2):
                return (None, 100000000000)
            elif connect4(grid, 1):
                return (None, -100000000000)
            else: # No move valid moves
                return (None, 0)
        else: # depth == 0:
            return (None, evalute_grid(grid))
    
    if maximizingPlayer:
        value = -float('inf')
        column = random.choice(options)
        for col in options:
            grid_copy = grid.copy()
            move(grid_copy,col,2)
            new_score = minimax(grid_copy, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else: # For the minimizing player i.e. PLAYER 1
        value = float('inf')
        column = random.choice(options)
        for col in options:
            grid_copy = grid.copy()
            move(grid_copy,col,1)
            new_score = minimax(grid_copy, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value
    
player = 1 # Player 1 goes first
game_over = False

while not game_over:

    if player == 1:

        col = input("Player 1 select column: ")
        move(grid, col, player)
        print(grid)
        if connect4(grid,player):
            print("Player 1 Wins!")
            game_over = True
        player = 2 # Move to Player 2
    
    else:

        col = minimax(grid, 5, -float('inf'), float('inf'), True)[0]

        move(grid, col, player)
        print(grid)
        if connect4(grid,player):
            print("Player 2 Wins!")
            game_over = True
        player = 1 # Move to Player 1