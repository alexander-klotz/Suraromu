from z3 import *
import re
import os

class SuraromuSolver:
    """
    @params:
    rows: integer representing the number of rows of the puzzle grid
    columns: integer representing the number of columns of the puzzle grid
    gateCellsVertical: Dictionairy containing all the vertical gates (int > 0 for ordered gates and int smaller 0 for unordered gates)
    gateCellsHorizontal: Dictionairy containing all the horizontal gates (int > 0 for ordered gates and int smaller 0 for unordered gates)
    blocked_cells: the blocked cells that are not allowed to be used (most of the time cells next to the gates)
    """
    def __init__(self, rows, columns, startIndex, gateCellsVertical, gateCellsHorizontal, blocked_cells):
        self.rows = rows
        self.columns = columns
        self.startIndex = startIndex
        self.gateCellsVertical = gateCellsVertical
        self.gateCellsHorizontal = gateCellsHorizontal
        self.blocked_cells = blocked_cells
        self.H = []
        self.V = []


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

        if(not gate_check):
            incorrect_loops.append(maybe_correct_loop)
            maybe_correct_loop = []

        return maybe_correct_loop, incorrect_loops


    """
    """
    def check_gate_ordering(self, cells, gate_cell_list):

        extractedGates = [cell for cell in cells if cell in gate_cell_list]
        #print(extractedGates)

        if(len(extractedGates) != len(self.gateCellsHorizontal) +  len(self.gateCellsVertical)):
            print("not all gates are visited in this loop")
            return False

        for idx, gate_cell in enumerate(extractedGates):
            idx = idx + 1
            expected_gate_cells = None
            if(self.gateCellsVertical.get(idx) != None):
                expected_gate_cells = self.gateCellsVertical.get(idx)
            if(self.gateCellsHorizontal.get(idx) != None):
                expected_gate_cells = self.gateCellsHorizontal.get(idx)
            if(expected_gate_cells == None):
                #print("nothing to check for index: ", idx)
                continue
            if(gate_cell not in expected_gate_cells):
                print(idx, gate_cell, expected_gate_cells)
                print("ordering not correct!!")
                return False
        print("!!!correct ordering")
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


    def getLoopCells(self, start_idx, usedEdges):
        loopCells = []

        usedEdges = usedEdges.copy()

        loopCells.append(start_idx)

        # get starting edges
        starting_edges = set(self.getConnectionsOfCell(*start_idx)).intersection(usedEdges)
        new_edge = starting_edges.pop()
        usedEdges.remove(new_edge)


        while(1):
            #print("cells ", loopCells, "   connectedCells ", getConnectedCells(new_edge), "   edge ", new_edge)
            connectedCell1, connectedCell2 = self.getConnectedCells(new_edge)
            if(connectedCell1 in loopCells):
                new_cell = connectedCell2
            elif(connectedCell2 in loopCells):
                new_cell = connectedCell1
            else:
                #print("error: ", connectedCell1, connectedCell2, loopCells, new_edge)
                break

            loopCells.append(new_cell)

            possibleConnOfCell = self.getConnectionsOfCell(*new_cell)
            maybe_new_edge = set(possibleConnOfCell).intersection(usedEdges)

            # check if we found a new edge
            if( len(maybe_new_edge) == 0 ):
                #print("no new edges found result is: ", loopCells)
                break

            new_edge = maybe_new_edge.pop()
            usedEdges.remove(new_edge)



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

        loopCount = 2
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

            correct_loop, incorrect_loops = self.getLoops(h_used, v_used, gate_cell_list)
            #self.print_grid(h_used, v_used)
            print(h_used, v_used)
            # remove the loops that do not start in the beginning
            #print("removed loops: ", incorrect_loops)
            blocked_loops_cond = []
            for incorrect_loop in incorrect_loops:
                blocked_loops_cond = blocked_loops_cond + [Or([Not(edge) for edge in incorrect_loop])]
                #print("inc loops:", incorrect_loop)
            s.add(blocked_loops_cond)


            if len(incorrect_loops) == 0 and correct_loop != []:
                
                print("!!!!!!!!!!solution found!!!!!!!!!", correct_loop)
                solutions.append(correct_loop)
                #os.system('clear')
                self.print_grid(h, v)
                
                # remove this solution
                blocking_clause = Not(And([var if bool(m[var]) else Not(var) for row in self.H for var in row] +
                                        [var if bool(m[var]) else Not(var) for row in self.V for var in row]))
                s.add(blocking_clause)

            if len(incorrect_loops) == 0 and correct_loop == []:
                break

            #print_grid(h, v)
            #print("\n----------------------------------------\n")
        
        return solutions



'''
# vertical means the line has to pass vertically (therefore the gate is a horizontal dotted line)
gcv =  {-68: [(3, 17)], -67: [(4, 17)], -27: [(16, 2)], -60: [(11, 17)], -49: [(19, 11)], -20: [(9, 2)], -9: [(3, 5)], -41: [(13, 11)], -55: [(19, 17)], -22: [(11, 2)], -34: [(12, 5)], -13: [(6, 8)]}
# since two gates share the same connection it might lead to an issue
gch = {-36: [(11, 7)], -65: [(5, 19)], -16: [(8, 6)], -18: [(8, 4)], -63: [(8, 18)], -5: [(2, 9)], -19: [(8, 3)], -69: [(2, 16)]}
# TODO: beforehand we MUST check if the highest gate value is not bigger than the smallest gate in total

blocked = [(1, 9), (1, 16), (3, 4), (3, 6), (3, 9), (3, 16), (3, 18), (4, 16), (4, 18), (4, 19), (6, 7), (6, 9), (6, 19), (7, 3), (7, 4), (7, 6), (7, 18), (9, 1), (9, 3), (9, 4), (9, 6), (9, 18), (10, 7), (11, 1), (11, 3), (11, 16), (11, 18), (12, 4), (12, 6), (12, 7), (13, 10), (13, 12), (16, 1), (16, 3), (19, 10), (19, 12), (19, 16), (19, 18)]


test = SuraromuSolver(21, 21, (5, 14), gcv, gch, blocked)
'''

#162 took very hard for humans
blocked = [(0, 11), (0, 15), (1, 1), (1, 4), (1, 8), (1, 13), (1, 17), (1, 20), (1, 23), (2, 6), (3, 1), (3, 3), (3, 5), (3, 6), (3, 10), (3, 12), (3, 14), (3, 17), (3, 20), (3, 22), (4, 8), (5, 3), (5, 7), (5, 8), (5, 13), (5, 23), (5, 24), (6, 1), (6, 5), (6, 9), (6, 16), (6, 18), (6, 20), (7, 7), (7, 9), (7, 12), (7, 16), (7, 22), (7, 23), (8, 1), (8, 2), (8, 5), (8, 18), (8, 20), (9, 5), (9, 6), (9, 8), (9, 12), (9, 14), (9, 18), (10, 3), (10, 10), (10, 12), (10, 16), (10, 18), (10, 19), (10, 23), (11, 1), (11, 5), (11, 7), (11, 8), (11, 10), (11, 14), (12, 1), (12, 8), (12, 12), (12, 16), (12, 18), (12, 22), (13, 3), (13, 4), (13, 6), (13, 10), (13, 14), (14, 4), (14, 8), (14, 12), (14, 16), (14, 19), (15, 0), (15, 2), (15, 6), (16, 4), (16, 9), (16, 10), (16, 12), (16, 16), (16, 20), (16, 22), (16, 23), (17, 0), (17, 2), (17, 6), (17, 14), (17, 16), (17, 20), (18, 4), (18, 8), (18, 12), (18, 14), (18, 18), (18, 22), (19, 6), (19, 10)]

gcv = {5: [(1, 2), (1, 3)], 7: [(3, 0)], 46: [(8, 19)], 24: [(9, 9), (9, 10), (9, 11)], 36: [(10, 24)], 11: [(11, 2), (11, 3), (11, 4)], 34: [(16, 24)], 16: [(17, 3), (17, 4), (17, 5)], -1: [(1, 5), (1, 6), (1, 7)], -2: [(1, 9), (1, 10), (1, 11), (1, 12)], -3: [(1, 14), (1, 15), (1, 16)], -4: [(1, 18), (1, 19)], -5: [(3, 7), (3, 8), (3, 9)], -6: [(3, 18), (3, 19)], -7: [(5, 0), (5, 1), (5, 2)], -8: [(5, 9), (5, 10), (5, 11), (5, 12)], -9: [(6, 17)], -10: [(7, 10), (7, 11)], -11: [(8, 21), (8, 22), (8, 23), (8, 24)], -12: [(9, 7)], -13: [(9, 15), (9, 16), (9, 17)], -14: [(10, 13), (10, 14), (10, 15)], -15: [(12, 9), (12, 10), (12, 11)], -16: [(12, 13), (12, 14), (12, 15)], -17: [(12, 19), (12, 20), (12, 21)], -18: [(13, 0), (13, 1), (13, 2)], -19: [(13, 5)], -20: [(14, 9), (14, 10), (14, 11)], -21: [(14, 13), (14, 14), (14, 15)], -22: [(14, 17), (14, 18)], -23: [(16, 0), (16, 1), (16, 2), (16, 3)], -24: [(16, 11)], -25: [(16, 13), (16, 14), (16, 15)], -26: [(17, 17), (17, 18), (17, 19)], -27: [(18, 0), (18, 1), (18, 2), (18, 3)], -28: [(18, 5), (18, 6), (18, 7)], -29: [(18, 9), (18, 10), (18, 11)], -30: [(18, 15), (18, 16), (18, 17)], -31: [(18, 19), (18, 20), (18, 21)]}
gch = {43: [(2, 20)], 39: [(2, 23), (3, 23), (4, 23)], 21: [(4, 5), (5, 5)], -32: [(4, 3)], -33: [(6, 3), (7, 3), (8, 3), (9, 3)], -34: [(15, 8), (16, 8), (17, 8)], -35: [(4, 20), (5, 20)], -36: [(0, 22), (1, 22), (2, 22)], -37: [(17, 23), (18, 23), (19, 23)]}

print(SuraromuSolver(20, 25, (7, 14), gcv, gch, blocked).solvePuzzle())





'''
# vertical means the line has to pass vertically (therefore the gate is a horizontal dotted line)
gcv =  {1: [(1, 3)], -67: [(1, 9)], -27: [(6, 0)], -60: [(8, 2)], -49: [(8, 4)], -20: [(8, 6)]}
# since two gates share the same connection it might lead to an issue
gch = {-36:  [(2, 8)], -65: [(4, 8)], -16: [(5, 1)], -18: [(9, 3)]}
# TODO: beforehand we MUST check if the highest gate value is not bigger than the smallest gate in total

blocked = [(1, 1), (1, 2), (1, 4), (1, 6), (1, 8), (2, 1), (2, 2), (3, 4), (3, 6), (3, 8), (4, 1), (4, 3), (5, 6), (5, 8), (6, 1), (6, 3), (6, 5), (7, 7), (7, 8), (8, 1), (8, 3), (8, 5), (8, 7), (8, 8)]


test = SuraromuSolver(10, 10, (0, 0), gcv, gch, blocked)

solutions = test.solvePuzzle()

print(solutions)

print(len(solutions))
'''