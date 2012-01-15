# ppjoin

ppjoin is a way of speeding up the exact set similarity problem (ssjoin) by reducing the number of candidate pairs that need a full check. [1] is a good introduction to the problem and solution.

Comparing n elements with each other using e.g. a Jaccard similarity function takes roughly n^2 comparison and is therefore prohibitively expensive. Using ppjoin the problem still scales quadratically but with a _much_ shallower slope, making the problem tractable on normal hardware.

The paper [1] describes various improvements (ppjoin+) which are not implemented here.

[1] http://www.cse.unsw.edu.au/~weiw/files/TODS-PPJoin-Final.pdf