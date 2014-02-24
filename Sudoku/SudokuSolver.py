#Sudoku Solver
"""
This version will take a text file with 9 rows of 9 numbers, or a single row of 81 numbers
zeros can be considered blank spots.  Spaces and returns are ignored
Will use depth first search to check if a square is possible then check the next square
****there should be ways to optimize along the road
"""

import sys
import fileinput
import os


def main():
	#will eventually have a stream reader to take directory, now hardcoded
	#sudokuFile = "test1.txt"
	sudokuFile = "test2easy.txt"

	#takes the file location and parses it into an array
	sudokuArray = parseFile(sudokuFile)
	#do something different if i have printed file does not exist
	"""
	print checkCol(8,80,sudokuArray)
	print checkRow(8,80,sudokuArray)
	print checkSquare(8,80,sudokuArray)
	print checkCol(9,80,sudokuArray)
	print checkRow(9,80,sudokuArray)
	print checkSquare(9,80,sudokuArray)
	print checkValidNumber(9,80,sudokuArray)
	"""
	

	#solves the puzzle and stores it into the solvedArray a 1d array of length 81
	solvedArray = sudokuSolver(sudokuArray)
	#prints the solved Array
	printResult(solvedArray)


def parseFile(sudokuFile):
	#if the file exists
	if os.path.exists(sudokuFile):
		#sudoku array is a 1d array of length 81 containing all numbers from the text file
		sudokuArray = []
		with open(sudokuFile) as f:
			#content is an array holding all of the lines in the file
			content = f.readlines()
			for aLine in content:
				#replaces line breaks and spaces
				aLine = aLine.replace("\n","")
				aLine = aLine.replace(" ","")
				#adds all numbers to the array
				for i in range(0,len(aLine)):
					sudokuArray.append(int(aLine[i]))
		if len(sudokuArray) == 81:
			return sudokuArray
		else:
			sys.exit("File Does Not Hold Correct Number of Values")
	else: 
		sys.exit("File Does Not Exist")

def sudokuSolver(sudokuArray):
	#current index of array
	slot = 0 
	#will hold tuple of slot and previously tried number
	previousAltered = []
	#boolean to know if made a mistake and need to backtrack
	goBack = True
	#variable to track where trial numbers should begin from, important when backtracking
	currentStart = 1
	#while program is unfinished
	while slot < len(sudokuArray):
		#if the current slot is blank
		if sudokuArray[slot] == 0:
			#try to fit in a number between the current start and 9 inclusive
			for i in range(currentStart,10):
				#checks the trial number to see if it passes the three sudoku critera
				if checkNumber(i, slot, sudokuArray):
					#if it passes then it is inserted into the array
					sudokuArray[slot] = i
					#the insertion is tracked by adding a tuple of the slot and number
					# to the previouslyAltered Array
					previousAltered.append((slot, i))
					slot +=1
					currentStart=1
					#number found that fits, don't need to go back
					goBack = False
					#breaks out of the for loop to continue on
					break
			#if all numbers have been tried in this slot in the current configuration
			#then must go back and backtrack
			if goBack:
				#last holds the tuple of the most recent addition to the array
				last = previousAltered.pop()
				#sets slot to the previously altered slot and set current start to 
				#one more than the number that was most recently tried in that slot
				slot = last[0]
				currentStart = last[1]+1
				#resets slot to zero
				sudokuArray[slot] = 0
			#if goBack is False, it's reset to true and the loop continues
			else: goBack = True
		#if the current slot is not zero go to the next slot
		else:
			slot +=1
	return sudokuArray
		
#Runs checks on the Col, Row, and Square
def checkNumber(entry, slot, sudokuArray):
	if not checkValidNumber(entry, slot, sudokuArray):
		return False
	else:
		return True
def checkValidNumber(current, slot, sudokuArray):
	#finds the column number of the current slot
	col = slot % 9
	row = slot/9
	#finds whether its the 1st 2nd or 3rd col or row in the square
	rowMod = row%3
	colMod = col%3
	#finds the upper left slot of the square
	first = slot-colMod-(rowMod*9)
	#finds all of the slots that correspond the the same column
	for key in range(col, len(sudokuArray), 9):
		#checks the current against all numbers in the column
		if sudokuArray[key] == current:
			return False
			#finds all slots that correspond to the same row
	for key in range(slot-col, slot-col+9):
		#checks current against all numbers in the row
		if sudokuArray[key] == current:
			return False
	#checks square
	for i in range(0,3):
		for j in range(0,3):
			key = first+j+(i*9)
			if sudokuArray[key] == current:
				return False
	return True
'''
#checks the trial entry in a particular slot to see if the col crieteria is passed
def checkCol(entry, slot, sudokuArray):
	#finds the column number of the current slot
	col = slot % 9
	#finds all of the slots that correspond the the same column
	for key in range(col, len(sudokuArray), 9):
		#checks the entry against all numbers in the column
		if sudokuArray[key] == entry:
			return False
	return True
#checks the trial entry in a particular slot to see if the row crieteria is passed	
def checkRow(entry, slot, sudokuArray):
	#finds the column number of the current slot
	col = slot % 9
	#finds all slots that correspond to the same row
	for key in range(slot-col, slot-col+9):
		#checks entry against all numbers in the row
		if sudokuArray[key] == entry:
			return False
	return True

#checks the trial entry in a particular slot to see if the square crieteria is passed
def checkSquare(entry, slot, sudokuArray):
	#finds the column and row
	col = slot % 9
	row = slot/9
	#finds whether its the 1st 2nd or 3rd col or row in the square
	rowMod = row%3
	colMod = col%3
	#finds the upper left slot of the square
	first = slot-colMod-(rowMod*9)
	for i in range(0,3):
		*************************BROKEN
		#checks top row of the square, left col of the square, and diag of square
		if (sudokuArray[first+i] == entry) or (sudokuArray[first+(i*9)]==entry) or (sudokuArray[first+i+(i*9)]==entry):
			return False
	return True
'''

#Prints the result in two ways, 9 lines of 9 numbers and the array itself
def printResult(solvedArray):
	line = ""
	counter = 0
	for i in solvedArray:
		if counter <9:
			line = line + str(i)
			counter +=1
		else:
			print line
			line = str(i)
			counter = 1
	print line
	print solvedArray

if __name__ == "__main__":
    main()























