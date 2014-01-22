#Sudoku Solver
"""
This version will take a text file with 9 rows of 9 numbers
zeros are blank spaces.
will use depth first search to check if a square is possible then check the next square
should be ways to optimize along the road
"""

import sys
import fileinput
import os


def main():
	#will eventually have a stream reader to take directory, now hardcoded
	sudokuFile = "test1.txt"
	sudokuArray = parseFile(sudokuFile)
	#do something different if i have printed file does not exist
	sudokuSolver(sudokuArray)


def parseFile(sudokuFile):
	if os.path.exists(sudokuFile):
		sudokuArray = []
		with open(sudokuFile) as f:
			content = f.readlines()
			for aLine in content:
				aLine = aLine.replace("\n","")
				cleanLine = []
				for i in range(0,len(aLine)):
					cleanLine.append(aLine[i])
				sudokuArray.append(cleanLine)
		return sudokuArray
	else: 
		print "file does not exist"

def sudokuSolver(sudokuArray):
	

if __name__ == "__main__":
    main()