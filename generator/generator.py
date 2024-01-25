import edges
import gates
from solverPrimWithPartConstraints_all import *
from loop import *
import random


'''
encoding of grid:
[b, l]
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
        puzzleGridFinal.chooseGates(4, gatesAmount, False)
        

        self.startIndex = puzzleGridFinal.startCell

        convertedVerticalSolverGates, convertedHorizontalSolverGates, blockedCells, self.grid = puzzleGridFinal.getGatesConverted()
        
        # don't use some rows and cols for blocked Cells to try and make the solution more interesting
        randRow = random.randrange(1, self.rows-1)
        randCol = random.randrange(1, self.cols-1)
        randRow2 = random.randrange(1, self.rows-1)
        randCol2 = random.randrange(1, self.cols-1)

        # insert blockedCells to try and create one solution
        if self.difficulty == "easy":
            for (i, j), cell in np.ndenumerate(self.grid):
                if i == randRow or j == randCol or i == randRow2 or j == randCol2:
                    continue
                if cell[0] == 0 and cell[1] == 0:
                    # empty cell so we add it to the blocked cells instead
                    if self.isNextToLoop((i, j)):
                        # 30% of the cells next to the loop we don't block in the beginning
                        if random.random() < 0.3/iteration:
                            continue
                    
                    blockedCells.append((i, j))
                    self.grid[(i, j)][0] = 2

               
        # TODO: fill in the gate cells that are not reachable not sure how we do this

        innerCounter = 0
        cellsToBlock = []


        while innerCounter < 10:

            innerCounter += 1
            # cells that are part of a gate we do not block
            cellsToBlock = [cellToBlock for cellToBlock in cellsToBlock if self.grid[cellToBlock][0] != 3 and self.grid[cellToBlock][0] != 4]
            
            # if we are in the second iteration there should be some cells we need to block
            blockedCells = blockedCells + cellsToBlock
            for r in range(self.rows):
                for c in range(self.cols):
                    if (r, c) in cellsToBlock:
                        self.grid[r, c][0] = 2

            
            solver = SuraromuSolverPrimWithPartConstraints(self.rows, self.cols, self.startIndex, convertedVerticalSolverGates, convertedHorizontalSolverGates, blockedCells, 54 - innerCounter*4)
            solutions = solver.solvePuzzle()
            
            if len(solutions) == 1:
                newBlockedCells = self.removeBlockedCells(blockedCells, convertedVerticalSolverGates, convertedHorizontalSolverGates)
                blockedCells = newBlockedCells
                convertedVerticalSolverGates, convertedHorizontalSolverGates, blockedCells = self.getMinimalGateOrdering(convertedVerticalSolverGates, convertedHorizontalSolverGates, blockedCells)
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

            if cellsToBlock != None:
                # we should have only a single solutions now but better to still check to make sure
                if innerCounter >= 5:
                    innerCounter -= 1
                continue

            # second way of trying to find cells that we should block
            bestFit, cellsToBlock = self.findLeastCommon(visitedCellsAllSolutions)

            if cellsToBlock == []:
                print("!Error! no cells to Block anymore to guarantee unique solution")
                return None, None, None, None, None, None, None

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
                diff = unionSet - set(solutionCells)
                return solutionsCells, list(diff)
        return None, None 


    def listCompare(self, listToCheck, remainingLists):
        return all( any(x in y for y in remainingLists) for x in listToCheck)

    def findLeastCommon(self, solutionsCells):
        setSolutionsCells = [set(l) for l in solutionsCells]
        
        unionSet = set.union(*setSolutionsCells)
        
        leastCommonList = None
        leastCommonCnt = float('inf')
        missingElements = None
        
        # iterate over each set
        for s in setSolutionsCells:
            # find the difference
            diff = unionSet - s
            
            # check if newly smallest set
            if len(diff) < leastCommonCnt:
                # update
                leastCommonCnt = len(diff)
                leastCommonList = list(s)
                missingElements = list(diff)
        
        return leastCommonList, missingElements

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


    def getMinimalGateOrdering(self, convertedVerticalSolverGates, convertedHorizontalSolverGates, blockedCells):
        
        for i in range(10):
            newConvertedVerticalSolverGates, newConvertedHorizontalSolverGates = convertedVerticalSolverGates.copy(), convertedHorizontalSolverGates.copy()

            removalAmount = int((len(newConvertedVerticalSolverGates) + len(newConvertedHorizontalSolverGates))*(1 - i/10))

            for j in range(removalAmount):
                self.chooseAndNegateDictKey(newConvertedVerticalSolverGates, newConvertedHorizontalSolverGates)

            solver = SuraromuSolverPrimWithPartConstraints(self.rows, self.cols, self.startIndex, newConvertedVerticalSolverGates, newConvertedHorizontalSolverGates, blockedCells, 2)
            solutions = solver.solvePuzzle()

            if len(solutions) == 1:
                return newConvertedVerticalSolverGates, newConvertedHorizontalSolverGates, blockedCells


        return convertedVerticalSolverGates, convertedHorizontalSolverGates, blockedCells

    def chooseAndNegateDictKey(self, gcv, gch):
        combined = {**gcv, **gch}
        
        # find keys > 0
        keysBiggerZero = [key for key in combined.keys() if key > 0]
        
        chosenKey = random.choice(keysBiggerZero)
        
        negChosenKey = chosenKey * -1
        
        if chosenKey in gcv:
            gcv[negChosenKey] = gcv.pop(chosenKey)
        else:
            gch[negChosenKey] = gch.pop(chosenKey)

    
    def removeBlockedCells(self, blockedCells, gcv, gch):
        newBlockedCells = blockedCells.copy()
        
        for cell in newBlockedCells:
            if not self.notGate(cell):
                continue
            verticalNeighbors = []
            horizontalNeighbors = []

            if 0 <= cell[0] - 1: verticalNeighbors.append((cell[0]-1, cell[1]))
            if cell[0] + 1 < self.rows: verticalNeighbors.append((cell[0]+1, cell[1]))
            
            if 0 <= cell[1] - 1: horizontalNeighbors.append((cell[0], cell[1]-1))
            if cell[1] + 1 < self.cols: horizontalNeighbors.append((cell[0], cell[1]+1))

            # check if both the cell below and above are non blocking cells
            if (len(verticalNeighbors) == 2 and not (verticalNeighbors[0] in newBlockedCells) and not (verticalNeighbors[1] in newBlockedCells)) or (
                len(horizontalNeighbors) == 2 and not (horizontalNeighbors[0] in newBlockedCells) and not (horizontalNeighbors[1] in newBlockedCells)):
                # try to remove this blocking cell
                newBlockedCells.remove(cell)
                # invoke solver and if only single solution keep this and return 
                solver = SuraromuSolverPrimWithPartConstraints(self.rows, self.cols, self.startIndex, gcv, gch, newBlockedCells, 2)
                solutions = solver.solvePuzzle()

                if len(solutions) == 1:
                    blockedCells = newBlockedCells.copy()
                else:
                    newBlockedCells = blockedCells.copy()
        
        return newBlockedCells


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



