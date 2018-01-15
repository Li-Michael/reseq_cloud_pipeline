#!/usr/bin/env python
#-*-coding:utf-8-*-

import sys,os
import random
import matplotlib.pyplot as plt

def countGenome(genome):
    import collections
    return collections.Counter(genome)

def longestCommonPrefix(s1, s2):
    i = 0
    while i < len(s1) and i < len(s2) and s1[i] == s2[i]:
        i += 1
    return s1[:i]

def qtoPhred33(q):
    """ Turn Q into Phred+33 ASCII-encoded quality"""
    return chr(q+33)

def qstoPhred33(qs):
    return [ ''.join(map(qtoPhred33,q)) for q in qs ]

def phred33toQ(qual):
    """ Trun Phred33 to integer according to ASCII table"""
    return ord(qual) -33

def phred33toQs(quals):
    return [ map(phred33toQ, q) for q in quals]

## read fastq file
def readFastq(filename):
    seqs = []
    quals = []
    with open(filename) as fh:
        while True:
            fh.readline()  # skip name line
            seq = fh.readline().strip()  # read base seqquence
            fh.readline()  # skip placeholder line
            qual = fh.readline().strip() # base quality line
            if len(seq) == 0:
                break
            seqs.append(seq)
            quals.append(qual)
        return seqs, quals

# qualities distribution
def qualDist(quals, figname="qualdist.png"):
    hist = [0]*len(quals[0])
    for qual in quals:
        for phred in qual:
            q = phred33toQ(phred)
            hist[q] += 1
    plt.bar(range(len(hist)), hist)
    plt.savefig(figname)
    return hist

## find the GC content by position
def findGCByPos(reads, figname="GC_pos.png"):
    GC_list = ['G','g','C','c']
    lenth = len(reads[0])
    gc = [0] * lenth
    total = 0
    for read in reads:
        for i in range(lenth):
            if read[i] in GC_list:
                gc[i] += 1
        total += 1
    
    for i in range(lenth):
        if total >0:
            gc[i] /= float(total)
    plt.plot(range(len(gc)), gc)
    plt.savefig(figname)
    
    return gc

## generate reads
def generateReads(genome, numReads, readLen):
    reads = []
    for _ in range(numReads):
        start = random.randint(0, len(genome)-readLen) - 1
        reads.append(genome[start:start+readLen])
    return reads

#complement = {'A':'T', 'T':'A', 'C':'G', 'G':'C', 'N':'N'}
complement = {'A':'T', 'T':'A', 'C':'G', 'G':'C'}
def reverseComplement(s):
    t = ''
    for base in s:
        t = complement[base] + t
    return t

## naive string match
def naive(p, t):
    occurrences = []
    #loop over alignments
    for i in range(len(t) - len(p) + 1):
        match = True
        #loop over characters
        for j in range(len(p)):
            #compare characters
            if not t[i+j] == p[j]:
                match = False  #mismatch; reject alignment
                break
        if match:
            occurrences.append(i) #all chars matched; record
    return occurrences

## naive string match with reverse complement
def naive_with_rc(p, t):
    matchs = naive(p, t)
    if not cmp(p,reverseComplement(p)):
        matchs.extend(naive(reverseComplement(p), t))
    
    return matchs


