import numpy as np
import random
from skimage.morphology import flood_fill

def getPosssibleCellIdxs(grid):
    goodBorderingIndices = []
    badBorderingIndices = []

    # offsets for neighboring cells
    neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # iterate all cells
    
    for i in range(1, grid.shape[0]-1):
        for j in range(1, grid.shape[1]-1):
            neighboringOnesCnt = 0
            if grid[i, j] == 0:

                # check the neighbors
                for dx, dy in neighbors:
                    x, y = i + dx, j + dy
                    if 0 < x < grid.shape[0]-1 and 0 < y < grid.shape[1]-1 and grid[x, y] == 1:
                        neighboringOnesCnt += 1
                
                # this is considered good since we want the loop to spread out
                if neighboringOnesCnt == 1:
                    goodBorderingIndices.append((i, j))
                # these are bad since they cause a clumped up loop
                elif neighboringOnesCnt > 1:
                    badBorderingIndices.append((i, j))

    return goodBorderingIndices, badBorderingIndices


'''
@param rows: number of rows for the final grid
@param cols: number of cols for the final grid
@param fillPercentage: percentage of grid that should be filled
@return: returns the grid with the inner part of the loop marked as 1s and the outer part marked as 0s
'''
def drawCycle(rows, cols, fillPercentage):
    # create array
    grid = np.zeros((rows, cols))

    # define random start cell
    startCell = (int(rows/2), int(cols/2))    # (random.randint(1, rows-2), random.randint(1, cols-2))
    grid[startCell] = 1


    # loop until criterion of fillPercentage is met
    while(np.count_nonzero(grid)/((rows-2)*(cols-2)) < fillPercentage):
        possGoodIdxs, possBadIdxs = getPosssibleCellIdxs(grid)
          
        goodCount = len(possGoodIdxs)
        badCount = len(possBadIdxs)
        
        if goodCount + badCount == 0 : break
        while True:
            
            if goodCount == 0:
                newCell = random.choice(possBadIdxs)
            elif badCount == 0:
                newCell = random.choice(possGoodIdxs)
            else:
                possList = possGoodIdxs+possBadIdxs
                newCell = possList[np.random.choice(len(possList), p=np.repeat([0.9/goodCount, 0.1/badCount], [goodCount, badCount]))]

            grid[newCell] = 1
            
            
            if np.all(flood_fill(grid, (0, 0), 3, connectivity=1)):
                break
            

            grid[newCell] = 0

            if np.count_nonzero(grid)/((rows-2)*(cols-2)) < fillPercentage:
                break
        
    
    # flood_fill the outside with 3s to find unreachable 0s
    grid = flood_fill(grid, (0, 0), 3, connectivity=1)
    grid[grid == 0] = 1
    grid[grid == 3] = 0
    #print_colored_grid(grid)

    return grid



# Function to print the grid with colored cells
def print_colored_grid(grid):
    # Define ANSI escape codes for colors
    GREEN = "\033[32m"  # Green text
    RED = "\033[31m"    # Red text
    RESET = "\033[0m"   # Reset text color
    for row in grid:
        for cell in row:
            if cell == 0:
                print(GREEN + "██" + RESET, end="")
            else:
                print(RED + "██" + RESET, end="")
        print()  # Move to the next row




def getCycleEdges(grid):
    # offsets for neighboring cells
    neighborUp = (-1, 0)
    neighborDown = (1, 0)
    neighborLeft = (0, -1)
    neighborRight = (0, 1)

    # init connection arrays
    verticalConnections = np.full((grid.shape[0] - 2, grid.shape[1] - 1), False)
    horizontalConnections = np.full((grid.shape[0] - 1, grid.shape[1] - 2), False)

    # iterate all cells
    for i in range(1, grid.shape[0]-1):
        for j in range(1, grid.shape[1]-1): 
            # if a cell is inside the loop check all four neighboring sides to determine if it is an outside cell 
            if grid[i, j] == 1:
                if grid[i + neighborUp[0], j + neighborUp[1]] == 0:
                    horizontalConnections[i - 1, j - 1] = True
                if grid[i + neighborDown[0], j + neighborDown[1]] == 0:
                    horizontalConnections[i , j - 1] = True
                if grid[i + neighborLeft[0], j + neighborLeft[1]] == 0:
                    verticalConnections[i - 1, j - 1] = True
                if grid[i + neighborRight[0], j + neighborRight[1]] == 0:
                    verticalConnections[i - 1, j] = True
                    
    
    return verticalConnections, horizontalConnections

def createLoop(rows, cols):
    loop = drawCycle(int(rows/2) + 1, int(cols/2) + 1, 0.7)
    loop = loop.repeat(2,axis=0).repeat(2,axis=1)
    V, H = getCycleEdges(loop)
    return loop, H, V
