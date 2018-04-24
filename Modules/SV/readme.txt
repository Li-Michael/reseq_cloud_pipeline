## Readme.txt-CNVnator
The output is as follows:

CNV_type coordinates CNV_size normalized_RD e-val1 e-val2 e-val3 e-val4 q0

normalized_RD -- normalized to 1.
e-val1        -- is calculated using t-test statistics.
e-val2        -- is from the probability of RD values within the region to be in
the tails of a gaussian distribution describing frequencies of RD values in bins.
e-val3        -- same as e-val1 but for the middle of CNV
e-val4        -- same as e-val2 but for the middle of CNV
q0            -- fraction of reads mapped with q0 quality

To have correct output of q0 field one needs to use the option -unique when extracting read mapping from bam/sam files.
