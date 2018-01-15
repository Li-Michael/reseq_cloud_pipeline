#!/usr/bin/env python
#-*-coding:utf-8-*-

import sys
import time,random
import math, numpy

n = int(sys.argv[1])

a = [random.randrange(10000) for i in range(n) ]
#a = [1,3,4,5,6,1,2,5,6,9]
## merg_sort

def merge(A, p, q, r):
    #n1 = q - p +1
    #n2 = r - q

    L = A[p:q] + [numpy.inf,]
    R = A[q:r] + [numpy.inf,]
    
    #print L,R
    i = j = 0
    for k in range(p,r):
        if L[i] <= R[j]:
            A[k] = L[i]
            i += 1
            #print i
        else:
            A[k] = R[j]
            j += 1
            #print j
    return A

def merge_sort(A, p,r):
    if p < r-1:
        q = int((r + p) /2)
        print q
        merge_sort(A, p, q)
        merge_sort(A, q, r)
        merge(A, p, q, r)
    return A

#aa1 = merge(a, 2,5,10)
aa = merge_sort(a, 0, len(a))
print aa
