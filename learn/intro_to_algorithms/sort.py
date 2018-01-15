#!/usr/bin/env python
#-*-coding:utf-8-*-

#######################
#  insertion sort && merge sort
#######################

import sys
import random,time
from numba import jit

n = int(sys.argv[1])

#nums = map(int,sin.split(","))
nums = [random.randrange(10000) for i in range(n)]
# 不重复一组随机数
# a = [random.sample([for i in range(10000)], n)]

#@jit
## insertion sort -1 
def sort_insert(nums):
    for i in range(n-1):
        sep = nums[i]
        for j in range(i+1,n):
            if nums[i] > nums[j]:
                nums[i] = nums[j]
                nums[j] = sep
    return nums

time1 = time.time()
nums = sort_insert(nums)
time2 = time.time()
#print nums

nums = [random.randrange(10000) for i in range(n)]
#print nums
## insertion sort -2 
time3 = time.time()
for j in range(1, n):
    key = nums[j]
    i = j-1
    while  i>=0 and nums[i] > key:
        nums[i+1] = nums[i]
        i = i-1
    nums[i+1] = key
time4 = time.time()

print "cost time: ", time2-time1, time4 - time3
#print "sort string: ", nums
