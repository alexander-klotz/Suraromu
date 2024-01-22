import numpy as np
import random


class edgeFunctions:

    def __init__(self, H, V):
        self.H = H
        self.V = V
        self.startIndex = None
        self.orderedEdges = None

    def getRandomStart(self):

        HandV = [self.H, self.V]
        isVertical = random.choice([0, 1])

        randomIndex = random.choice(np.transpose(np.where(HandV[isVertical])))
        #print("Random index as start:", [isVertical, randomIndex])
        return np.concatenate(([isVertical], randomIndex))


    '''
    @returns a List of ordered edge indexes with each index consisting of [v, r, c] 
        where v = if it's a vertical 1 and if its a horizontal 0
            r = row of the edge
            c = column of the edge
    '''
    def getOrderedEdges(self):

        orderedList = []
        self.startIndex = self.getRandomStart()

        vIdxs, hIdxs = self.getNextIdxs(self.startIndex[1], self.startIndex[2], self.startIndex[0])
        # (Create array that contains visited connections or) simply delete the visited Trues and WHILE we still find a new True keep on collecting
        prevIdx = self.startIndex
        nextIdx = self.startIndex

        for vIdx in vIdxs:
            if self.V[vIdx] == True:
                nextIdx = np.concatenate(([1], vIdx)) 
                break

        for hIdx in hIdxs:
            if self.H[hIdx] == True:
                nextIdx = np.concatenate(([0], hIdx)) 
                break

        while(True):

            orderedList.append(prevIdx)
            
            if prevIdx[0] == 1:
                self.V[prevIdx[1], prevIdx[2]] = False
            else:
                self.H[prevIdx[1], prevIdx[2]] = False
            
            prevIdx = nextIdx

            vIdxs, hIdxs = self.getNextIdxs(nextIdx[1], nextIdx[2], nextIdx[0])
            for vIdx in vIdxs:
                if self.V[vIdx] == True:
                    
                    nextIdx = np.concatenate(([1], vIdx)) 
                    break

            for hIdx in hIdxs:
                if self.H[hIdx] == True:
                    
                    nextIdx = np.concatenate(([0], hIdx)) 
                    break
            
            
            if (prevIdx==nextIdx).all():
                if prevIdx[0] == 1:
                    self.V[prevIdx[1], prevIdx[2]] = False
                else:
                    self.H[prevIdx[1], prevIdx[2]] = False
                orderedList.append(prevIdx)
                break
        
        self.orderedEdges = orderedList

        return orderedList




    def getNextIdxs(self, row, col, isVertical):

        def checkAppend(shape, list, idx):
            if 0 <= idx[0] < shape[0] and 0 <= idx[1] < shape[1]:
                list.append(idx)

        verticalNexts, horizontalNexts = [], []
        if isVertical:
            # next one is still vertical
            checkAppend(self.V.shape, verticalNexts, (row-1, col))
            checkAppend(self.V.shape, verticalNexts, (row+1, col))
            
            # next one is horizontal
            checkAppend(self.H.shape, horizontalNexts, (row, col))
            checkAppend(self.H.shape, horizontalNexts, (row+1, col))
            checkAppend(self.H.shape, horizontalNexts, (row, col-1))
            checkAppend(self.H.shape, horizontalNexts, (row+1, col-1))
        else:
            # next one is still horizontal
            checkAppend(self.H.shape, horizontalNexts, (row, col-1))
            checkAppend(self.H.shape, horizontalNexts, (row, col+1))
            
            # next one is vertical
            checkAppend(self.V.shape, verticalNexts, (row, col))
            checkAppend(self.V.shape, verticalNexts, (row-1, col))
            checkAppend(self.V.shape, verticalNexts, (row, col+1))
            checkAppend(self.V.shape, verticalNexts, (row-1, col+1))
        return verticalNexts, horizontalNexts

