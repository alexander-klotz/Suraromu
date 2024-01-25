from z3 import *
import re
import os

class SuraromuSolverPrimWithPartConstraints:
    """
    @params:
    rows: integer representing the number of rows of the puzzle grid
    columns: integer representing the number of columns of the puzzle grid
    gateCellsVertical: Dictionairy containing all the vertical gates (int > 0 for ordered gates and int smaller 0 for unordered gates)
    gateCellsHorizontal: Dictionairy containing all the horizontal gates (int > 0 for ordered gates and int smaller 0 for unordered gates)
    blocked_cells: the blocked cells that are not allowed to be used (most of the time cells next to the gates)
    solutionsRequired: integer that specifies the amount of solutions that should be found
    """
    def __init__(self, rows, columns, startIndex, gateCellsVertical, gateCellsHorizontal, blocked_cells, solutionsRequired):
        self.rows = rows
        self.columns = columns
        self.startIndex = startIndex
        self.gateCellsVertical = gateCellsVertical
        self.gateCellsHorizontal = gateCellsHorizontal
        self.blocked_cells = blocked_cells
        self.H = []
        self.V = []
        self.solutionsRequired = solutionsRequired


    def print_grid(self, h, v):

        for i in range(2*self.rows - 1):

            if(i % 2 == 0):
                # horizontal lines
                print("\n", end=" ")
                for h_line in h[int(i/2)]:
                    if(str(h_line) == "True"):
                        print("──", end=' ')
                    else:
                        print("  ", end=' ')
            else:
                # vertical lines
                print(" ")
                for v_line in v[int(i/2)]:
                    if(str(v_line) == "True"):
                        print("| ", end=' ')
                    else:
                        print("  ", end=' ')
    
    def print_grid_color(self, h, v, wrongParts):

        convertedWrongParts = [[self.getEdgeIdxAndDirection(edge) for edge in wrongPart] for wrongPart in wrongParts]

        colors = [
            '\033[30m',  # Black
            '\033[31m',  # Red
            '\033[32m',  # Green
            '\033[33m',  # Yellow
            '\033[34m',  # Blue
        ]

        def find_element_in_2d_list(lst, element):
            for i, sublist in enumerate(lst):
                if element in sublist:
                    return i
            return -1

        # Reset color to default
        reset_color = '\033[0m'

        for i in range(2*self.rows - 1):

            if(i % 2 == 0):
                # horizontal lines
                print("\n", end=" ")
                for idx, h_line in enumerate(h[int(i/2)]):
                    colorIndex = find_element_in_2d_list(convertedWrongParts, ((int(i/2), idx), True))
                    if colorIndex == -1:
                        if(str(h_line) == "True"):
                            print("─~", end=' ')
                        else:
                            print("  ", end=' ')
                    else:
                        if(str(h_line) == "True"):
                            print(colors[colorIndex%5] + "──" + reset_color, end=' ')
                        else:
                            print("  ", end=' ')
            else:
                # vertical lines
                print(" ")
                for idx, v_line in enumerate(v[int(i/2)]):
                    colorIndex = find_element_in_2d_list(convertedWrongParts, ((int(i/2), idx), False))
                    if colorIndex == -1:
                        if(str(v_line) == "True"):
                            print("|.", end=' ')
                        else:
                            print("  ", end=' ')
                    else:
                        if(str(v_line) == "True"):
                            print(colors[colorIndex%5] + "| " + reset_color, end=' ')
                        else:
                            print("  ", end=' ')

    def getWrongParts(self, main_loop_visited_cells, gate_cell_list):
            wrongParts = []

            main_loop_visited_cells = list(dict.fromkeys(main_loop_visited_cells))
            if main_loop_visited_cells[0] != self.startIndex:
                main_loop_visited_cells = [self.startIndex] + main_loop_visited_cells
            if main_loop_visited_cells[-1] != self.startIndex:
                main_loop_visited_cells.append(self.startIndex)
            
            start = 0
            currentGateCount = 0
            lastGateVisited = None
            totalVisitedGates = 0

            # Iterate over the main path first cell is always the start cell and therefore we can skip that
            for i in range(len(main_loop_visited_cells)):
                if i == 0: continue

                if totalVisitedGates == len(self.gateCellsHorizontal) + len(self.gateCellsVertical):
                    # here we just check if the part from the last known gate till the start is correct once we have all the other gates
                    if totalVisitedGates - currentGateCount != lastGateVisited and currentGateCount + 1 != lastGateVisited:
                        wrongParts.append(main_loop_visited_cells[start:])
                        break

                if main_loop_visited_cells[i] in gate_cell_list:
                    # we are at a gateCell, get the key
                    currentGateNumber = 0
                    totalVisitedGates += 1
                    for key, value in {**self.gateCellsHorizontal, **self.gateCellsVertical}.items():
                        if main_loop_visited_cells[i] in value:
                            currentGateNumber = key

                    if currentGateNumber < 0:
                        # unordered gate
                        currentGateCount += 1
                    
                    if currentGateNumber > 0:
                        # we reached an ordered gate now we have to check if this subpart was correct
                        currentGateCount += 1
                        if start == 0:
                            # special case if we still are at the start
                            if currentGateCount == currentGateNumber or len(self.gateCellsHorizontal) + len(self.gateCellsVertical) - currentGateCount + 1 == currentGateNumber:
                                # the ordering of this part is correct so we look at the rest starting from this cell
                                start = i
                                currentGateCount = 0
                            else:
                                # ordering is incorrect add it to the incorrect parts and increase start and set currentGateCount to 0
                                wrongParts.append(main_loop_visited_cells[start:i+1])
                                start = i
                                currentGateCount = 0

                        else:
                            # normal case where we are somewhere in the middle
                            if abs(currentGateNumber - lastGateVisited) == currentGateCount:
                                # the ordering of this part is correct so we look at the rest starting from this cell
                                start = i
                                currentGateCount = 0
                            else:
                                # ordering is incorrect add it to the incorrect parts and increase start and set currentGateCount to the gate we are just at
                                wrongParts.append(main_loop_visited_cells[start:i+1])
                                start = i
                                currentGateCount = 0
                        lastGateVisited = currentGateNumber


            return wrongParts


    def getConnectionsOfCell(self, r, c):
        cellConnections = []

        if(r > 0):
            cellConnections.append(self.V[r-1][c])

        if(r < self.rows-1):
            cellConnections.append(self.V[r][c])

        if(c > 0):
            cellConnections.append(self.H[r][c-1])

        if(c < self.columns-1):
            cellConnections.append(self.H[r][c])

        return cellConnections


    """
    @idx = index of the connection that has been made
    @isHorizontal = determines if the connection is horizontal or not

    @returns the connections of the cells that have just been connected (TODO: make concrete decision if we omit the
    current connection that we made at index idx (probably better since that way our logic stays smaller))

    @Example h_1_1 has been made therefore we return the connections of cell 1,1 and cell 1,2
    @Example v_1_1 has been made therefore we return the connections of cell 1,1 and cell 2,1
    """
    def getFollowingConnections(self, idx, isHorizontal):

        connections = [[], []]

        if(isHorizontal):
            # we made a horizontal connection
            connections[0] = self.getConnectionsOfCell(*idx)
            connections[1] = self.getConnectionsOfCell(idx[0], idx[1] + 1)
            # removing the current element we just connected
            connections[0] = [ele for ele in connections[0] if str(ele) != "h_%s_%s" % (idx[0], idx[1])]
            connections[1] = [ele for ele in connections[1] if str(ele) != "h_%s_%s" % (idx[0], idx[1])]
        else:
            # we made a vertical connection
            connections[0] = self.getConnectionsOfCell(*idx)
            connections[1] = self.getConnectionsOfCell(idx[0] + 1, idx[1])
            # removing the current element we just connected
            connections[0] = [ele for ele in connections[0] if str(ele) != "v_%s_%s" % (idx[0], idx[1])]
            connections[1] = [ele for ele in connections[1] if str(ele) != "v_%s_%s" % (idx[0], idx[1])]
        return connections


    def getLoops(self, h, v, gate_cell_list):
        maybe_correct_loop = []
        incorrect_loops = []

        allUsedEdges = set()
        for h_sub in h:
            for h_single in h_sub:
                allUsedEdges.add(h_single)
        for v_sub in v:
            for v_single in v_sub:
                allUsedEdges.add(v_single)


        maybe_correct_loop = self.getLoopOfCell(self.startIndex, allUsedEdges)

        main_loop_visited_cells = self.getLoopCells(self.startIndex, allUsedEdges)

        gate_check = self.check_gate_ordering(main_loop_visited_cells, gate_cell_list) or self.check_gate_ordering(reversed(main_loop_visited_cells), gate_cell_list)

        remainingEdges = allUsedEdges.difference(maybe_correct_loop)

        while (len(remainingEdges) > 0):
            # get a single loop
            sample_edge = remainingEdges.pop()
            remainingEdges.add(sample_edge)
            idxSampleEdge, orient = self.getEdgeIdxAndDirection(sample_edge)
            incorrect_loop = self.getLoopOfCell(idxSampleEdge, remainingEdges)

            # remove the edges of that loop from remaining
            remainingEdges = remainingEdges.difference(incorrect_loop)

            # add the single loop to the incorrect loops
            incorrect_loops.append(incorrect_loop)

        wrongPartsEdges = []
        # try to extract some parts we can exclude
        extractedGates = [cell for cell in main_loop_visited_cells if cell in gate_cell_list]
    
        if (len(extractedGates) == len(self.gateCellsHorizontal) +  len(self.gateCellsVertical)):
            # the main loop that we found traverses all gates so we can try to find some incorrect parts
            wrongPartsCells = self.getWrongParts(main_loop_visited_cells, gate_cell_list)
            for wrongPartCells in wrongPartsCells:
                wrongPartEdges = []
                for i in range(len(wrongPartCells) - 1):
                    wrongPartEdges.append(self.getCommonConnection(wrongPartCells[i], wrongPartCells[i+1]))
                wrongPartsEdges.append(wrongPartEdges)
            

        if(not gate_check):
            incorrect_loops.append(maybe_correct_loop)
            maybe_correct_loop = []

        return maybe_correct_loop, incorrect_loops, wrongPartsEdges



    def check_gate_ordering(self, cells, gate_cell_list):

        extractedGates = [cell for cell in cells if cell in gate_cell_list]

        if(len(extractedGates) != len(self.gateCellsHorizontal) +  len(self.gateCellsVertical)):
            return False

        for idx, gate_cell in enumerate(extractedGates):
            idx = idx + 1
            expected_gate_cells = None
            if(self.gateCellsVertical.get(idx) != None):
                expected_gate_cells = self.gateCellsVertical.get(idx)
            if(self.gateCellsHorizontal.get(idx) != None):
                expected_gate_cells = self.gateCellsHorizontal.get(idx)
            if(expected_gate_cells == None):
                continue
            if(gate_cell not in expected_gate_cells):
                return False
        return True


    """
    idx index of cell of which we want to get the connected loop
    @returns List of all the edges that are in this loop
    """
    def getLoopOfCell(self, idx, usedEdges):
        loopElements = set()
        new_edges = ((set(self.getConnectionsOfCell(*idx))).intersection(usedEdges)).difference(loopElements)

        while(len(new_edges) != 0):
            loopElements = loopElements.union(new_edges)

            acc_new_edges = set()
            for edge in new_edges:
                first_neighbours, second_neighbours = self.getFollowingConnections(*self.getEdgeIdxAndDirection(edge))
                all_neighbours = set(first_neighbours).union(set(second_neighbours))
                acc_new_edges = acc_new_edges.union( all_neighbours.intersection(usedEdges).difference(loopElements) )
            new_edges = acc_new_edges.copy()
        return loopElements


    def getCommonConnection(self, cell1, cell2):
        commonElements = set(self.getConnectionsOfCell(*cell1)) & set(self.getConnectionsOfCell(*cell2))
        return list(commonElements)[0]

    def getLoopCells(self, start_idx, usedEdges):
        loopCells = []

        usedEdges = usedEdges.copy()

        loopCells.append(start_idx)

        # get starting edges
        starting_edges = set(self.getConnectionsOfCell(*start_idx)).intersection(usedEdges)
        new_edge = starting_edges.pop()
        usedEdges.remove(new_edge)


        while(1):
            connectedCell1, connectedCell2 = self.getConnectedCells(new_edge)
            if(connectedCell1 in loopCells):
                new_cell = connectedCell2
            elif(connectedCell2 in loopCells):
                new_cell = connectedCell1
            else:
                break

            loopCells.append(new_cell)

            possibleConnOfCell = self.getConnectionsOfCell(*new_cell)
            maybe_new_edge = set(possibleConnOfCell).intersection(usedEdges)

            # check if we found a new edge
            if( len(maybe_new_edge) == 0 ):
                break

            new_edge = maybe_new_edge.pop()
            usedEdges.remove(new_edge)


        loopCells = list(dict.fromkeys(loopCells))
        if loopCells[0] != self.startIndex:
            loopCells = [self.startIndex] + loopCells
        if loopCells[-1] != self.startIndex:
            loopCells.append(self.startIndex)
        return loopCells


    def getConnectedCells(self, edge):
        ints = list(map(int, re.findall(r'\d+', str(edge))))

        if(str(edge)[0] == "h"):
            return (ints[0], ints[1]), (ints[0], ints[1] + 1)

        return (ints[0], ints[1]), (ints[0] + 1, ints[1])



    """
    given an edge @e like h_11_2
    @returns th idx (11, 2) and a bool for the orientation
    """
    def getEdgeIdxAndDirection(self, e):
        ints = list(map(int, re.findall(r'\d+', str(e))))
        return (ints[0], ints[1]), str(e)[0] == "h"


    def solvePuzzle(self):

        gate_cell_list = []
        for value in self.gateCellsHorizontal.values():
            gate_cell_list += value

        for value in self.gateCellsVertical.values():
            gate_cell_list += value


        # Matrix of Bool values representing the horizontal movement [r][c-1]
        self.H = [ [ Bool("h_%s_%s" % (i, j)) for j in range(self.columns-1) ]
            for i in range(self.rows) ]

        # Matrix of Bool values representing the vertical movement [r-1][c]
        self.V = [ [ Bool("v_%s_%s" % (i, j)) for j in range(self.columns) ]
            for i in range(self.rows-1) ]


        # create condition that makes starting line from starting point
        start_cond = [ PbEq([(x, 1) for x in self.getConnectionsOfCell(*self.startIndex)], 2) ]

        # create condition so for each line there will be exactly one neighboring line
        line_cond_h = []
        for r in range(self.rows):
            for c in range(self.columns-1):
                first_neighbours, second_neighbours = self.getFollowingConnections((r, c), True)
                line_cond_h.append( Implies(self.H[r][c], And(PbEq([(add_c, 1) for add_c in first_neighbours], 1), PbEq([(add_c, 1) for add_c in second_neighbours], 1))))


        line_cond_v = []
        for r in range(self.rows-1):
            for c in range(self.columns):
                first_neighbours, second_neighbours = self.getFollowingConnections((r, c), False)
                line_cond_v.append( Implies(self.V[r][c], And(PbEq([(add_c, 1) for add_c in first_neighbours], 1), PbEq([(add_c, 1) for add_c in second_neighbours], 1))))



        blocked_cond = []
        [ [ blocked_cond.append(Not(con)) for con in self.getConnectionsOfCell(*blocked_cell)] for blocked_cell in self.blocked_cells]


        h_cond = []
        h_block_cond = []
        h_cond_complete = []
        for key, gate_cells in self.gateCellsHorizontal.items():
            for gate_cell in gate_cells:
                r = gate_cell[0]
                c = gate_cell[1]
                h_cond.append(And(self.H[r][c-1], self.H[r][c]))

                blocked_gate_cond = []
                if(r > 0):
                    blocked_gate_cond.append(Not(self.V[r-1][c]))

                if(r < self.rows-1):
                    blocked_gate_cond.append(Not(self.V[r][c]))

                h_block_cond.append( And(blocked_gate_cond) )

            h_cond_complete.append(PbEq([(gate, 1) for gate in h_cond], 1))
            h_cond = []


        v_cond = []
        v_cond_complete = []
        v_block_cond = []
        for key, gate_cells in self.gateCellsVertical.items():
            for gate_cell in gate_cells:
                r = gate_cell[0]
                c = gate_cell[1]
                v_cond.append(And(self.V[r-1][c], self.V[r][c]))

                blocked_gate_cond = []
                if(c > 0):
                    blocked_gate_cond.append(Not(self.H[r][c-1]))

                if(c < self.columns-1):
                    blocked_gate_cond.append(Not(self.H[r][c]))

                v_block_cond.append( And(blocked_gate_cond) )

            v_cond_complete.append(PbEq([(gate, 1) for gate in v_cond], 1))
            v_cond = []


        gate_cond = h_cond_complete + v_cond_complete + h_block_cond + v_block_cond




        s = Solver()
        s.add(start_cond + line_cond_h + line_cond_v + blocked_cond + gate_cond)

        incorrect_loops = [1]
        solutions = []

        while s.check() == sat:
            m = s.model()
            h = [ [ m.evaluate(self.H[i][j]) for j in range(self.columns-1) ]
                for i in range(self.rows) ]
            v = [ [ m.evaluate(self.V[i][j]) for j in range(self.columns) ]
                for i in range(self.rows-1) ]

            # TODO: find loops that are not connected with starting point


            h_used = [ [ self.H[i][j] for j in range(self.columns-1) if m.evaluate(self.H[i][j]) ]
                for i in range(self.rows)]
            v_used = [ [ self.V[i][j] for j in range(self.columns) if m.evaluate(self.V[i][j]) ]
                for i in range(self.rows-1) ]

            correct_loop, incorrect_loops, wrongParts = self.getLoops(h_used, v_used, gate_cell_list)
            blocked_loops_cond = []
            for incorrect_loop in incorrect_loops:
                blocked_loops_cond = blocked_loops_cond + [Or([Not(edge) for edge in incorrect_loop])]
            s.add(blocked_loops_cond)
            
            for wrongPart in wrongParts:
                partBlocking = Not(And(wrongPart))
                s.add(partBlocking)


            if len(incorrect_loops) == 0 and correct_loop != []:
                
                solutions.append((self.convert_boolrefs_to_booleans(h), self.convert_boolrefs_to_booleans(v)))

                # prematurely return the solutions to make the time the solver takes up shorter
                if len(solutions) >= self.solutionsRequired:
                    return solutions

                # remove this solution
                blocking_clause = Not(And([var if bool(m[var]) else Not(var) for row in self.H for var in row] +
                                        [var if bool(m[var]) else Not(var) for row in self.V for var in row]))
                s.add(blocking_clause)

            if len(incorrect_loops) == 0 and correct_loop == []:
                break

        return solutions
    
    def convert_boolrefs_to_booleans(self, boolref_list):
        return [[str(boolref) == "True" for boolref in inner_list] for inner_list in boolref_list]

