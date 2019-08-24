#!/usr/bin/python

import sys

def pyramid(n):
    counter=0
    for i in range(1,n+1):
        if (i%2 == 1):
           counter=counter+1
        else:
           counter=counter+2

        print("* "*counter)

def usage():
   print("Usage: ./pyramid.py NUMBER_OF_LINES [e.g. ./pyramid.py 6]\n")
   sys.exit()

# Main - Execution Starts here 
if(len(sys.argv) < 2):
   usage()

n=int(sys.argv[1])
pyramid(n)
