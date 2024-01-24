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
                print(len(blockedCells))
                newBlockedCells = self.removeBlockedCells(blockedCells, convertedVerticalSolverGates, convertedHorizontalSolverGates)
                blockedCells = newBlockedCells
                print(len(blockedCells))
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


    def getMinimalGateOrdering(self, convertedVerticalSolverGates, convertedHorizontalSolverGates, blockedCells):
        
        for i in range(1, 5):
            newConvertedVerticalSolverGates, newConvertedHorizontalSolverGates = convertedVerticalSolverGates.copy(), convertedHorizontalSolverGates.copy()

            removalAmount = int((len(newConvertedVerticalSolverGates) + len(newConvertedHorizontalSolverGates))/i)

            for j in range(removalAmount):
                self.chooseAndNegateDictKey(newConvertedVerticalSolverGates, newConvertedHorizontalSolverGates)

            solver = SuraromuSolverPrimWithPartConstraints(self.rows, self.cols, self.startIndex, newConvertedVerticalSolverGates, newConvertedHorizontalSolverGates, blockedCells)
            solutions = solver.solvePuzzle()

            if len(solutions) == 1:
                return newConvertedVerticalSolverGates, newConvertedHorizontalSolverGates, blockedCells


        return convertedVerticalSolverGates, convertedHorizontalSolverGates, blockedCells

    def chooseAndNegateDictKey(self, gcv, gch):
        # Combine the two dictionaries
        combined = {**gcv, **gch}
        
        # Filter keys greater than 0
        keys_greater_than_zero = [key for key in combined.keys() if key > 0]
        
        # If no keys are greater than 0, return None
        if not keys_greater_than_zero:
            print("ERROR!!!!!")
            return None, None, None
        
        # Randomly select a key
        selected_key = random.choice(keys_greater_than_zero)
        
        # Multiply the selected key by -1
        negated_key = selected_key * -1
        
        # Replace the selected key in the original dictionary
        if selected_key in gcv:
            gcv[negated_key] = gcv.pop(selected_key)
        else:
            gch[negated_key] = gch.pop(selected_key)

    
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
            if len(verticalNeighbors) == 2 and not (verticalNeighbors[0] in newBlockedCells) and not (verticalNeighbors[1] in newBlockedCells):
                # try to remove this blocking cell
                newBlockedCells.remove(cell)
                print(cell)
                # invoke solver and if only single solution keep this and return 
                solver = SuraromuSolverPrimWithPartConstraints(self.rows, self.cols, self.startIndex, gcv, gch, newBlockedCells)
                solutions = solver.solvePuzzle()

                if len(solutions) == 1:
                    blockedCells = newBlockedCells.copy()
                    print("CELLLLL: ", cell)
                else:
                    newBlockedCells = blockedCells.copy()
                
                continue
            
            # check if both the cell to the right and left are non blocking cells
            if len(horizontalNeighbors) == 2 and not (horizontalNeighbors[0] in newBlockedCells) and not (horizontalNeighbors[1] in newBlockedCells):
                # try to remove this blocking cell
                newBlockedCells.remove(cell)
                print(cell)
                
                # invoke solver and if only single solution keep this and return 
                solver = SuraromuSolverPrimWithPartConstraints(self.rows, self.cols, self.startIndex, gcv, gch, newBlockedCells)
                solutions = solver.solvePuzzle()

                if len(solutions) == 1:
                    blockedCells = newBlockedCells.copy()
                    print("CELLLLL: ", cell)
                else:
                    newBlockedCells = blockedCells.copy()
        
        return newBlockedCells
            
            

    '''this does not work since the self.grid is not updated.... 
    maybe instead search for blocked cells for whitch two neighbours are non blockedCell (check using in blockedCells) and then try to remove that 
    def removeLineOfBlockedCells(self, blockedCells, gcv, gch):
        newBlockedCells = blockedCells.copy()
        linesToTry = (self.rows + self.cols)/20
        randomRows = list(range(1, self.rows-1))
        random.shuffle(randomRows)
        randomCols = list(range(1, self.cols-1))
        random.shuffle(randomCols)

        for rRow in randomRows:
            for rCol in randomCols:
                # try to remove all the blocked Cells in both the row and the column
                insideLoop = False
                removed = False
                print(len(newBlockedCells))
                for c in range(self.cols):
                    if self.grid[(rRow, c)][0] != 2:
                        insideLoop = True
                    
                    if insideLoop:
                        if self.grid[(rRow, c)][0] == 2 and self.notGate((rRow, c)):
                            print((rRow, c))
                            if (rRow, c) in newBlockedCells: 
                                newBlockedCells.remove((rRow, c))
                                removed = True
                    if removed and self.grid[(rRow, c)][1] != 0:
                        print(self.grid[(rRow, c)])
                        break
                    
                    #TODO: make it so we end off the next time we hit the loop

                insideLoop = False
                removed = False
                for r in range(self.rows):
                    if self.grid[(r, rCol)][0] != 2:
                        insideLoop = True
                    
                    if insideLoop:
                        if self.grid[(r, rCol)][0] == 2 and self.notGate((r, rCol)):
                            print((r, rCol))
                            if (r, rCol) in newBlockedCells: 
                                newBlockedCells.remove((r, rCol))
                                removed = True
                    if removed and self.grid[(r, rCol)][1] != 0:
                        print(self.grid[(r, rCol)])
                        break
                
                # revoke solver and if only single solution keep this and return 
                solver = SuraromuSolverPrimWithPartConstraints(self.rows, self.cols, self.startIndex, gcv, gch, newBlockedCells)
                solutions = solver.solvePuzzle()

                if len(solutions) == 1:
                    print(len(newBlockedCells))
                    print("removed: ", rRow, rCol)
                    return newBlockedCells
                else:
                    newBlockedCells = blockedCells.copy()
        return blockedCells
    '''  
        


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



