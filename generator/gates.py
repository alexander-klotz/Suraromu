import numpy as np
import random

'''
horizontal gate here means the gate line is horizontal!!!
'''
class PuzzleGrid:

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
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

        self.grid = np.empty((rows, cols), dtype=object)
        self.orderedCells = []
        self.startCell = None
        self.possibleGates = []     # these still need to be checked for collisions with eachother
        
        '''
        list of elements build like: (isHorizontal, startOfGate, endOfGate, cells, idx(ordering idx), x(gate number))       
        '''
        self.placedGates = []

    def initialFillGrid(self, orderedConnections):
        
        for r in range(self.rows):
            for c in range(self.cols):
                self.grid[r, c] = [0, 0]
        
        self.startCell = self.getCommonCell(orderedConnections[0], orderedConnections[-1])
        startCellLine = self.getCellLine(orderedConnections[0], orderedConnections[-1])
        self.grid[self.startCell][0] = 1
        self.grid[self.startCell][1] = startCellLine
        self.orderedCells.append(self.startCell)
        
        for i in range(len(orderedConnections)-1):
            cellIdx = self.getCommonCell(orderedConnections[i], orderedConnections[i+1])
            cellLine = self.getCellLine(orderedConnections[i], orderedConnections[i+1])
            self.grid[cellIdx][1] = cellLine
            self.orderedCells.append(cellIdx)
        return self.orderedCells


    def getCommonCell(self, combinedIndex1, combinedIndex2):
        cells1 = self.getCells(combinedIndex1)
        cells2 = self.getCells(combinedIndex2)
        commonCells = [cell for cell in cells1 if cell in cells2]
        return commonCells[0]


    '''
    0... no line
    1... vertical line
    2... horizontal line
    3... ┛
    4... ┗
    5... ┓
    6... ┏

    '''
    def getCellLine(self, combinedIndex1, combinedIndex2):
        if combinedIndex1[0] == combinedIndex2[0]:
            if combinedIndex1[0] == 1:
                return 1
            else:
                return 2
       
        else:
            horizontalIndex, verticalIndex = (combinedIndex1, combinedIndex2) if combinedIndex1[0] == 0  else (combinedIndex2, combinedIndex1)
            
            if horizontalIndex[1] > verticalIndex[1]:
                if horizontalIndex[2] < verticalIndex[2]:
                    return 3
                else:
                    return 4
            else:
                if horizontalIndex[2] < verticalIndex[2]:
                    return 5
                else:
                    return 6


    def getCells(self, combinedIndex):
        cells = []
        if combinedIndex[0] == 1:
            # vertical connection
            cells.append((combinedIndex[1], combinedIndex[2]))
            cells.append((combinedIndex[1]+1, combinedIndex[2]))
        else:
            # horizontal connection
            cells.append((combinedIndex[1], combinedIndex[2]))
            cells.append((combinedIndex[1], combinedIndex[2]+1))
             
        return cells
    
    def getPossibleGate(self, row, col):

        isHorizontal = False

        if self.grid[row, col][1] == 1:
                    isHorizontal = True
                    leftLimit = col
                    rightLimit = col
                    while(leftLimit > 0 and self.grid[row, leftLimit-1][1] == 0):
                        leftLimit -= 1
                    while(rightLimit < self.cols-1 and self.grid[row, rightLimit+1][1] == 0):
                        rightLimit += 1
                    if leftLimit == rightLimit:
                        return 0, 0, 0, None
                    return leftLimit, rightLimit, row, isHorizontal

        if self.grid[row, col][1] == 2:
                    topLimit = row
                    bottomLimit = row
                    while(topLimit > 0 and self.grid[topLimit-1, col][1] == 0):
                        topLimit -= 1
                    while(bottomLimit < self.rows-1 and self.grid[bottomLimit+1, col][1] == 0):
                        bottomLimit += 1
                    if topLimit == bottomLimit:
                        return 0, 0, 0, None
                    return topLimit, bottomLimit, col, isHorizontal
        return 0, 0, 0, None

    
    def initializeOrderedPossibleGates(self):
        for idx in self.orderedCells:
            if idx == self.startCell:
                continue
            lowerlimit, upperlimit, otherdim, isHorizontal = self.getPossibleGate(*idx)
            if isHorizontal is None:
                continue
            else:
                if isHorizontal:
                    # check if the gate has space for a blocked cell or is on the very edge of the puzzle (both isHorizontal and !isHorizontal)
                    if (lowerlimit < idx[1] or lowerlimit == 0) and (upperlimit > idx[1] or upperlimit == self.cols-1):
                        self.possibleGates.append((lowerlimit, upperlimit, idx, isHorizontal))
                else:
                    if (lowerlimit < idx[0] or lowerlimit == 0) and (upperlimit > idx[0] or upperlimit == self.rows-1):
                        self.possibleGates.append((lowerlimit, upperlimit, idx, isHorizontal))
        return
    
    
    def chooseGates(self, maxLength, count, difficulty, placeAll):

        # try to place given amount (count) of gates using random sampling
        gatesToTry = []
        if len(self.possibleGates) < count:
            # not enough gates
            for idx, gate in enumerate(self.possibleGates):
                gatesToTry.append((idx, gate)) 
        else:
            # choose count random gates and note their index
            randomIndices = random.sample(range(len(self.possibleGates)), count)

            for index in randomIndices:
                gate = self.possibleGates[index]
                gatesToTry.append((index, gate))

        for gateToTry in gatesToTry:
            idx, currGate = gateToTry
            lowerlimit, upperlimit, lineIdx, isHorizontal = currGate
            startOfGate, endOfGate, cells = self.tryPlaceGate(lowerlimit, upperlimit, lineIdx, isHorizontal)
            if len(cells) < 2 or (len(cells) == 2 and startOfGate is not None and endOfGate is not None) or startOfGate == lineIdx or endOfGate == lineIdx:
                continue
            
            newStartOfGate, newEndOfGate, newCells = self.shortenGate(startOfGate, endOfGate, cells, lineIdx, maxLength)
            self.placedGates.append((isHorizontal, newStartOfGate, newEndOfGate, newCells, idx, 0))
            
            # fill in the needed cells
            for cell in newCells:
                if isHorizontal:
                    self.grid[cell][0] = 4
                else:
                    self.grid[cell][0] = 3
            if newStartOfGate is not None:
                self.grid[newStartOfGate][0] = 2
            if newEndOfGate is not None:
                self.grid[newEndOfGate][0] = 2
            count -= 1       

        
        if placeAll:
            # we start off by placing all possible gates
            for idx, currGate in enumerate(self.possibleGates):
                if idx in [usedGates[0] for usedGates in gatesToTry]:
                    continue
                lowerlimit, upperlimit, lineIdx, isHorizontal = currGate
                startOfGate, endOfGate, cells = self.tryPlaceGate(lowerlimit, upperlimit, lineIdx, isHorizontal)
                if len(cells) < 2 or (len(cells) == 2 and startOfGate is not None and endOfGate is not None) or startOfGate == lineIdx or endOfGate == lineIdx:
                    continue
                
                newStartOfGate, newEndOfGate, newCells = self.shortenGate(startOfGate, endOfGate, cells, lineIdx, maxLength)
                self.placedGates.append((isHorizontal, newStartOfGate, newEndOfGate, newCells, idx, 0))
                # fille in the needed cells
                for cell in newCells:
                    if isHorizontal:
                        self.grid[cell][0] = 4
                    else:
                        self.grid[cell][0] = 3
                if newStartOfGate is not None:
                    self.grid[newStartOfGate][0] = 2
                if newEndOfGate is not None:
                    self.grid[newEndOfGate][0] = 2

                count -= 1
                
                if count == 0:
                    break

        return ""
    
    def shortenGate(self, startOfGate, endOfGate, cells, lineIdx, maxLength):

        randMaxLength = random.randint(1, maxLength)
        length = len(cells)
        if startOfGate != None: length -= 1
        if endOfGate != None: length -= 1

        while length > randMaxLength:
            front = random.choice([True, False])
            if front:
                if cells[0] == lineIdx:
                    continue
                if startOfGate is not None and cells[1] < lineIdx:
                    cells = cells[1:]
                    length -= 1
                if startOfGate is None:
                    length -= 1
                startOfGate = cells[0]
                 
            else:
                if cells[-1] == lineIdx:
                    continue
                if endOfGate is not None and cells[-2] > lineIdx:
                    cells = cells[:-1]
                    length -= 1
                
                if endOfGate is None:
                    length -= 1
                endOfGate = cells[-1]
            
        return startOfGate, endOfGate, cells

    def tryPlaceGate(self, lowerlimit, upperlimit, lineIdx, isHorizontal):

        # these two store where we need to place black cells
        startOfGate = None
        endOfGate = None
        cells = [lineIdx]
        if isHorizontal:
            for col in range(lineIdx[1] - 1, lowerlimit - 1, -1):
                if col == 0:
                     # no black cell needed since it's on the very edge and we stop here
                    cells.insert(0, (lineIdx[0], 0))
                else:    
                    if self.grid[lineIdx[0], col][0] == 0 and self.grid[lineIdx[0], col][1] == 0:
                        # we can place a gate to here
                        cells.insert(0, (lineIdx[0], col))
                        if col == lowerlimit:
                            startOfGate = (lineIdx[0], col)
                    elif self.grid[lineIdx[0], col][0] == 2:
                        # blocked cell so we need to stop here
                        cells.insert(0, (lineIdx[0], col))
                        startOfGate = (lineIdx[0], col)
                        break
                    else:
                        # we can not expand the gate further so we are done
                        startOfGate = (lineIdx[0], col + 1)
                        break
            
            for col in range(lineIdx[1] + 1, upperlimit + 1):
                if col == self.cols - 1:
                     # no black cell needed since it's on the very edge and we stop here
                    cells.append((lineIdx[0], self.cols - 1))
                else:    
                    if self.grid[lineIdx[0], col][0] == 0 and self.grid[lineIdx[0], col][1] == 0:
                        # we can place a gate to here
                        cells.append((lineIdx[0], col))
                        if col == upperlimit:
                            endOfGate = (lineIdx[0], col)
                    elif self.grid[lineIdx[0], col][0] == 2:
                        # blocked cell so we need to stop here
                        cells.append((lineIdx[0], col))
                        endOfGate = (lineIdx[0], col)
                        break
                    else:
                        # we can not expand the gate further so we are done
                        endOfGate = (lineIdx[0], col - 1)
                        break

        else:
            for row in range(lineIdx[0] - 1, lowerlimit - 1, -1):
                if row == 0:
                     # no black cell needed since it's on the very edge and we stop here
                    cells.insert(0, (0, lineIdx[1]))
                else:    
                    if self.grid[row, lineIdx[1]][0] == 0 and self.grid[row, lineIdx[1]][1] == 0:
                        # we can place a gate to here
                        cells.insert(0, (row, lineIdx[1]))
                        if row == lowerlimit:
                            startOfGate = (row, lineIdx[1])
                    elif self.grid[row, lineIdx[1]][0] == 2:
                        # blocked cell so we need to stop here
                        cells.insert(0, (row, lineIdx[1]))
                        startOfGate = (row, lineIdx[1])
                        break
                    else:
                        # we can not expand the gate further so we are done
                        startOfGate = (row+1, lineIdx[1])
                        break
            
            for row in range(lineIdx[0] + 1, upperlimit + 1):
                if row == self.rows - 1:
                    # no black cell needed since it's on the very edge and we stop here
                    cells.append((self.rows - 1, lineIdx[1]))
                else:    
                    if self.grid[row, lineIdx[1]][0] == 0 and self.grid[row, lineIdx[1]][1] == 0:
                        # we can place a gate to here
                        cells.append((row, lineIdx[1]))
                        if row == upperlimit:
                            endOfGate = (row, lineIdx[1])
                    elif self.grid[row, lineIdx[1]][0] == 2:
                        # blocked cell so we need to stop here
                        cells.append((row, lineIdx[1]))
                        endOfGate = (row, lineIdx[1])
                        break
                    else:
                        # we can not expand the gate further so we are done
                        endOfGate = (row-1, lineIdx[1])
                        break
        
        
        return startOfGate, endOfGate, cells

    def getGatesConverted(self):
        convertedHorizontalSolverGates = {} 
        convertedVerticalSolverGates = {}
        blockedCells = []
        '''
        list of elements build like: (isHorizontal, startOfGate, endOfGate, cells, idx(ordering idx), x(gate number))       
        '''
        for orderedIdx, gate in enumerate(sorted(self.placedGates, key=lambda x: x[4])):
            isHorizontal, startOfGate, endOfGate, cells, idx, x = gate
            onlyGateCells = cells
            
            x = orderedIdx + 1
            if x == 0:
                # gate order is not given
                x = -idx

            # the solver doesn't need the black cells of the gates
            if startOfGate is not None:
                onlyGateCells = onlyGateCells[1:]
            if endOfGate is not None:
                onlyGateCells = onlyGateCells[:-1]

            if isHorizontal:
                # here we have to switch this aroud since the solver has another definition of horizontal
                convertedVerticalSolverGates[x] = onlyGateCells
            else:
                convertedHorizontalSolverGates[x] = onlyGateCells
        
        # get the blocked cells
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r, c][0] == 2:
                    blockedCells.append((r, c))
        



        return convertedVerticalSolverGates, convertedHorizontalSolverGates, blockedCells, self.grid


    def printGrid(self):
        for r in range(self.rows):
            for c in range(self.cols):
                print(["+", "┃", "━", "┛", "┗", "┓", "┏"][self.grid[r, c][1]], end="")

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

