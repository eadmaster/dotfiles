#!/bin/sed -f
# original table from  https://www.ocf.berkeley.edu/~beno/nfpager.html  http://www.pagercodes.com/pager-code-alphabet.html

# convert to uppercase
s/.*/\U&/

s/A/6/g
#s/A/8/g
s/B/8/g
s/C/5/g
#s/C/0/g
s/D/0/g
s/E/3/g
s/F/3/g
s/G/9/g
#s/G/6/g
s/H/4/g
s/I/1/g
s/J/7/g
s/K/15/g
s/L/7/g
#s/L/1/g
s/M/177/g
s/N/17/g
s/O/0/g
s/P/9/g
s/Q/9/g
#s/Q/0/g
s/R/12/g
s/S/5/g
s/T/7/g
s/U/11/g
#s/U/4/g
s/V/11/g
#s/V/4/g
s/W/111/g
#s/W/44/g
s/X/25/g
s/Y/4/g
s/Z/2/g

# symbols
#s/,/ /g
#s/./ /g
s/?/2/g
s/!/1/g
s/\./-/g

