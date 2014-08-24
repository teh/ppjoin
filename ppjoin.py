# coding: utf8

"""
Copyright 2012 Thomas Hunger. All rights reserved.
Licenced under the 2-clause BSD license ("Simplified BSD License" or "FreeBSD License")
Code taken from https://github.com/teh/ppjoin
"""

import re
import collections
import math
from itertools import groupby

def prefix_length(s, threshold):
    return len(s) - int(math.ceil(threshold*len(s))) + 1

def overlap_constraint(len_s1, len_s2, threshold):
    return int(math.ceil(threshold / (1.0 + threshold) * (len_s1 + len_s2)))

def jaccard(a, b):
    return 1.0 * len(a & b) / len(a | b)

def candidate_pairs(records, t):
    """
    Implementation of ppjoin with slight variations from:

    http://www.cse.unsw.edu.au/~weiw/files/TODS-PPJoin-Final.pdf
    """
    ii = collections.defaultdict(set) # inverted index
    cp = set() # candidate pairs

    for xr_index, xr in enumerate(records):
        if not xr:
            continue
        xp = prefix_length(xr, t)
        overlap_by_yr = collections.defaultdict(int)
        for i in range(xp):
            xr_element = xr[i]
            for yr_index, j in ii[xr_element]:
                yr = records[yr_index]
                if len(yr) < t * len(xr):
                    continue
                alpha = overlap_constraint(len(xr), len(yr), t)
                upper_bound = 1 + min(len(xr) - i, len(yr) - j)
                # count how many items of yr overlap xr:
                if overlap_by_yr[yr_index] + upper_bound >= alpha:
                    overlap_by_yr[yr_index] += 1
                else:
                    overlap_by_yr[yr_index] = 0

            ii[xr_element].add((xr_index, i))

        # check overlap in suffixes
        for yr_index, overlap in overlap_by_yr.iteritems():
            yr = records[yr_index]
            yp = prefix_length(yr, t)
            wx = xr[xp - 1]
            wy = yr[yp - 1]
            alpha = overlap_constraint(len(xr), len(yr), t)
            if wx < wy:
                ubound = overlap + len(xr) - xp;
                if ubound >= alpha:
                    overlap += len(set(xr[xp:]) & set(yr[overlap+1:]))
            else:
                ubound = overlap + len(yr) - yp;
                if ubound >= alpha:
                    overlap += len(set(xr[overlap:]) & set(yr[yp+1:]))
            if overlap >= alpha:
                cp.add((xr_index, yr_index))

    return cp

def prepare_strings(list_of_strings):
    records = [re.findall(u'\w+', x.lower(), re.UNICODE) for x in list_of_strings]

    records = map(lambda x: normalize_words(x), records)

    # no argsort, so we have to fake it:
    # argsort[i] will point to the original data index before sorting.
    argsort = sorted(range(len(records)), key=lambda x: len(records[x]))
    records.sort(key=len)

    elements = list(y for r in records for y in r)
    order_map = dict(
        (el, i)
        for i, (el, count) in enumerate(sorted(collections.Counter(elements).iteritems(), key=lambda x:x[1]))
    )

    records_sorted = [sorted(x, key=lambda x: order_map[x]) for x in records]
    return records, records_sorted, argsort


def normalize_words(words):
	"""
	Normalize same words in document to unique words tokens as described in
	the paper. Use "@#" to split the word and index of the word.
	"""
	words.sort()
	tmp = [list(g) for k, g in groupby(words)]

	wwi = map(lambda ws: [x + "@#" + str(i) for i, x in enumerate(ws)], tmp)
	return [w for same_words in wwi for w in same_words]
						 
