#!/usr/bin/env python
#-*-coding:utf-8-*-

import sys


def editDistRecursive(x, y):
    """ this implementation is very slow """
    if len(x) == 0:
        return len(y)
    elif len(y) == 0:
        return len(x)
    else:
        distHor = editDistRecursive(x[:-1], y) + 1
        distVer = editDistRecursive(x, y[:-1]) + 1
        if x[-1] == y[-1]:
            distDiag = editDistRecursive(x[:-1], y[:-1])
        else:
            distDiag = editDistRecursive(x[:-1], y[:-1]) + 1
    return min(distDiag, distHor, distVer)


## editDistance(x, y):
def editDistance(x ,y):
    """ use dynamic programming for edit distance, every edit distance = 1 """
    # init matrix D
    D = [[0]*(len(y)+1)] * (len(x)+1)
    """ 
    D = []
    for i in range(len(x)+1):
        D.append([0] * (len(y)+1))
    """
    
    for i in range(len(x)+1):
        D[i][0] = i
    for i in range(len(y)+1):
        D[0][i] = i

    for i in range(1, len(x)+1):
        for j in range(1, len(y)+1):
            editHor = D[i][j-1] + 1
            editVer = D[i-1][j] + 1
            if x[i-1] == y[i-1]:
                editDiag = D[i-1][j-1]
            else:
                editDiag = D[i-1][j-1] + 1
            D[i][j] = min(editHor, editVer, editDiag)
    return D[-1][-1]

## penalty matrix  A C G T
alphabet = ['A', 'C', 'G', 'T']
penalty_score = [[0, 4, 2, 4, 8], \
                 [4, 0, 4, 2, 8], \
                 [2, 4, 0, 4, 8], \
                 [4, 2, 4, 0, 8], \
                 [8, 8, 8, 8, 8] ]

def globalAlignment(x ,y):
    """ use dynamic programming and score matrix for global alignment """
    D = []
    for i in range(len(x)+1):
        D.append([0]*(len(y)+1))

    for i in range(1, len(x)+1):
        D[i][0] = D[i-1][0] + penalty_score[alphabet.index(x[i-1])][-1]
    for i in range(1, len(y)+1):
        D[0][i] = D[0][i-1] + penalty_score[-1][alphabet.index(y[i-1])]
   
    for i in range(1, len(x)+1):
        for j in range(1, len(y)+1):
            editHor = D[i][j-1] + penalty_score[-1][alphabet.index(y[j-1])]
            editVer = D[i-1][j] + penalty_score[alphabet.index(x[i-1])][-1]
            editDiag = D[i-1][j-1] + penalty_score[alphabet.index(x[i-1])][alphabet.index(y[j-1])]
            D[i][j] = min(editHor, editVer, editDiag)
    
    return D[-1][-1]
    






