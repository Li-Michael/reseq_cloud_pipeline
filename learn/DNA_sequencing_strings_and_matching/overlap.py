import sys

def overlap(a, b, min_length=3):
    """ return length of longest suffix of 'a' matching
        a prefix of 'b' that is at least 'min_length' 
        character long. If no such overlap exists, return 0. """
    assert a != '' and b != ''
    start = 0   # start all the way at the left
    for i in range(min_length, len(a)):
        start =  a.find(b[:min_length], start)  # look for b's suffix in a
        if start == -1:   ## no more occurrences to left 
            return 0
        elif b.startswith(a[start:]):  ## found occurrence; check if full prefix/suffix match
            return len(a) -start
        start += 1  ## move just past previous match
        
from itertools import permutations
def naive_overlap(reads, k=3):
    """ find all overlaps in reads """
    overlaps = {}
    for a,b in permutations(reads, 2):
        overlen = overlap(a, b, min_length=k)
        if overlen >0:
            overlaps[(a, b)] = overlen
    return overlaps


def kmer_overlap(reads, k=3):
    """ use k-mer dictionary to find all overlaps in reads. faster """
    kmer_dict = {}
    overlaps = {}
    for read in reads:
        for i in range(len(read)-k+1):
            if read[i:i+k] not in kmer_dict:
                kmer_dict[read[i:i+k]] = []
            kmer_dict[read[i:i+k]].append(read)
    
    for v in kmer_dict.values():
        for a,b in permutations(v,2):
            overlen = overlap(a,b,min_length=k)
            if overlen>0:
                overlaps[(a,b)] = overlen

    return overlaps
        



