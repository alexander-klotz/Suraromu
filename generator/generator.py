import edges
import gates
from solverPrimWithPartConstraints_all import *
from loop import *
import random


'''
encoding of grid:
[b, l, x]
b (all the black things):
    0... no black element
    1... start cell
    2... blocked cell
    3... vertical gate line
    4... horizontal gate line
l (all the grey lines):
    0... no line
    1... vertical line
    2... horizontal line
    3... ┛
    4... ┗
    5... ┓
    6... ┏
x (gate number if needed):
    x... gate number (maybe only for the end blocks or for all blocks)
'''

class Generator:
    def __init__(self, rows, cols, difficulty):
        self.rows = rows
        self.cols = cols
        self.difficulty = difficulty
        self.H = None
        self.V = None
        self.startIndex = None
        self.orderedEdges = None
        self.grid = None

    def generate(self, iteration):
        
        
        loop, H, V = createLoop(self.rows, self.cols)

        edgeFunctions = edges.edgeFunctions(H, V)
        orderedEdges = edgeFunctions.getOrderedEdges()

        gatesAmount = int(len(orderedEdges) / (5 - 0.2 * iteration))

        puzzleGridFinal = gates.PuzzleGrid(self.rows, self.cols)
        puzzleGridFinal.initialFillGrid(orderedEdges)
        puzzleGridFinal.initializeOrderedPossibleGates()        
        puzzleGridFinal.chooseGates(4, gatesAmount, 3, False)
        
        
        # printing
        puzzleGridFinal.printGrid()
        puzzleGridFinal.printGates()

        self.startIndex = puzzleGridFinal.startCell

        convertedVerticalSolverGates, convertedHorizontalSolverGates, blockedCells, self.grid = puzzleGridFinal.getGatesConverted()
        
        # for easy difficulty just place a bunch of black cells maybe even all possible ones and then just call the solver to check if only one solution remains

        randRow = random.randrange(1, self.rows-1)
        randCol = random.randrange(1, self.cols-1)
        randRow2 = random.randrange(1, self.rows-1)
        randCol2 = random.randrange(1, self.cols-1)
        if self.difficulty == "easy":
            for (i, j), cell in np.ndenumerate(self.grid):
                if i == randRow or j == randCol or i == randRow2 or j == randCol2:
                    continue
                if cell[0] == 0 and cell[1] == 0:
                    # empty cell so we add it to the blocked cells instead
                    if self.isNextToLoop((i, j)):
                        if random.random() < 0.3/iteration:
                            continue
                    
                    blockedCells.append((i, j))
                    self.grid[(i, j)][0] = 2

               
        # TODO: fill in the gate cells that are not reachable not sure how we do this


        # TODO: try to remove some gateCell ordering and see if we still have a single solution

        innerCounter = 0
        cellsToBlock = []

        #self.printGrid()

        while innerCounter < 5:

            innerCounter += 1
            # cells that are part of a gate we do not block
            cellsToBlock = [cellToBlock for cellToBlock in cellsToBlock if self.grid[cellToBlock][0] != 3 and self.grid[cellToBlock][0] != 4]
            
            # randomly remove some to maybe find a less filled out solution
            if innerCounter < 2:
                cellsToBlock = random.sample(cellsToBlock, len(cellsToBlock) // 2)
            
            # if we are in the second iteration there should be some cells we need to block
            blockedCells = blockedCells + cellsToBlock
            for r in range(self.rows):
                for c in range(self.cols):
                    if (r, c) in cellsToBlock:
                        print(r, c)
                        self.grid[r, c][0] = 2

            self.printGates()
            
            solver = SuraromuSolverPrimWithPartConstraints(self.rows, self.cols, self.startIndex, convertedVerticalSolverGates, convertedHorizontalSolverGates, blockedCells)
            solutions = solver.solvePuzzle()
            
            if len(solutions) == 1:
                print("done only one solution remains")
                # TODO!!!!: try the solver with (all the) gates in unordered to get a bit of a harder puzzle probably...
                return self.rows, self.cols, self.startIndex, convertedVerticalSolverGates, convertedHorizontalSolverGates, blockedCells, solutions[0]

            if len(solutions) == 0:
                print("!Error! no solution anymore")
                return None, None, None, None, None, None, None

            # try to find out which cells we can block
            visitedCellsAllSolutions = []
            for solution in solutions:
                HSol, VSol = solution
                visitedCellsAllSolutions.append(self.getCells(HSol, VSol))

            # first try to find a bestFit for which all other lists contain atleast one other element and if not such list exists
            singleSolution, cellsToBlock = self.tryToFindUnique(visitedCellsAllSolutions)
            # filter the cellsToBlock

            if cellsToBlock != None:
                # we should have only a single solutions now but better to still check to make sure
                if innerCounter >= 5:
                    innerCounter -= 1
                continue

            # second way of trying to find cells that we should block
            bestFit, cellsToBlock = self.find_least_common(visitedCellsAllSolutions)

            if cellsToBlock == []:
                print("!Error! no cells to Block anymore to guarantee unique solution")
                return None, None, None, None, None, None, None

        print("no unique solution found after ", innerCounter, " iterations")
        return None, None, None, None, None, None, None

        
       
    def isNextToLoop(self, index):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up

        for dr, dc in directions:
            newRow, newCol = index[0] + dr, index[1] + dc
            if 0 <= newRow < self.rows and 0 <= newCol < self.cols:
                if self.grid[(newRow, newCol)][1] != 0:
                    return True
                
        return False
    
    def tryToFindUnique(self, solutionsCells):
        unionSet = set.union(*([set(l) for l in solutionsCells]))
        for idx, solutionCells in enumerate(solutionsCells):
            if self.listCompare(solutionCells, solutionsCells[:idx] + solutionsCells[idx + 1:]):
                print("\n\n--------FOUND SOLUTION THAT CAN BE SINGULAR--------\n\n")
                diff = unionSet - set(solutionCells)
                return solutionsCells, list(diff)
        return None, None 


    def listCompare(self, listToCheck, remainingLists):
        return all( any(x in y for y in remainingLists) for x in listToCheck)

    def find_least_common(self, solutionsCells):
        # Create a set for each list
        set_solutionsCells = [set(l) for l in solutionsCells]
        
        # Find the union of all sets
        union_set = set.union(*set_solutionsCells)
        
        # Initialize variables
        least_common_list = None
        least_common_count = float('inf')
        missing_elements = None
        
        # Iterate over each set
        for s in set_solutionsCells:
            # Find the difference between the union set and the current set
            diff = union_set - s
            
            # If the size of the difference is less than the least common count
            if len(diff) < least_common_count:
                # Update the least common count and list
                least_common_count = len(diff)
                least_common_list = list(s)
                missing_elements = list(diff)
        
        print(least_common_list, missing_elements)
        return least_common_list, missing_elements

    '''
    check if a blocked cell is part of a gate
    '''
    def notGate(self, idx):
        r, c = idx
        
        # belongs to vertical gate
        if r-1 >= 0 and self.grid[r-1, c][0] == 3:
            return False
        if r+1 < self.rows and self.grid[r+1, c][0] == 3:
            return False
        
        # belongs to horizontal gate
        if c-1 >= 0 and self.grid[r, c-1][0] == 4:
            return False
        if c+1 < self.cols and self.grid[r, c+1][0] == 4:
            return False
        
        return True

    def getCells(self, H, V):
        cellsUnique = set()
        for r, hRow in enumerate(H):
            for c, h in enumerate(hRow):
                if h:
                    cells = self.getBothCells(r, c, "h")
                    for cell in cells:
                        cellsUnique.add(cell)
        
        for r, vRow in enumerate(V):
            for c, v in enumerate(vRow):
                if v:
                    cells = self.getBothCells(r, c, "v")
                    for cell in cells:
                        cellsUnique.add(cell)
        return list(cellsUnique)

    def getBothCells(self, r, c, orient):
        if orient == "h":
            return [(r, c), (r, c+1)]
        else:
             return [(r, c), (r+1, c)]


    def printGrid(self):
        for r in range(self.rows):
            for c in range(self.cols):
                print(["+", "┃", "━", "┛", "┗", "┓", "┏"][self.grid[r, c][1]], end="")

            print("")

    def printLoop(self, visited):
        for r in range(self.rows):
            for c in range(self.cols):
                if (r, c) in visited:
                    print("+", end="")
                else:
                    print(" ", end="")

            print("")

    '''
    0... no black element
    1... start cell
    2... blocked cell
    3... vertical gate line
    4... horizontal gate line
    '''
    def printGates(self):
        for r in range(self.rows):
            for c in range(self.cols):
                print([". ", "s ", "██", "┃ ", "━━"][self.grid[r, c][0]], end="")

            print("")



