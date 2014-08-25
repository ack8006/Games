#SudokuSolver
#Alex Takata
#8/25/2014
 
#when started, the program will prompt the user for a text file of the sudoku
#puzzle.  The text file can be formatted either in a 
#continuous string of digits row by row, or in 9 lines.
#If there is a solution the program will print it.  If there is no solution the program 
#will state that there is no valid solution and prompt for another file. If
#there are multiple solution the program will state that and prompt for another
#file.
 
import os
import sys
 
def main():
	fileName = raw_input('Enter filename: ')
	#converts text file to array
	sudokuArray = parseFile(fileName)
	#attempts to solve sudoku puzzle
	sudokuArray = sudokuSolver(list(sudokuArray))
	#if solution, prints solved puzzle
	printResult(sudokuArray)
 
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
				for i in xrange(0,len(aLine)):
					#will try to append the character as an int, but if it can't will except and exit
					try:
						sudokuArray.append(int(aLine[i]))
					except ValueError:
						print "File Contains non-integer values"
						exit()
		if len(sudokuArray) == 81:
			return sudokuArray
		else:
			print "File Does Not Hold Correct Number of Values"
			main()
	else: 
		print "File Does Not Exist"
		main()

def sudokuSolver(sudokuArray):
	#worst case performance for the brute force solver is a puzzle where clues are heavily loaded to one side
	#as the solver doesn't look forward.  to speed it up will start from more crowded half of puzzle
	topCount = 0
	bottomCount = 0
	for slot in xrange(0,80):
		if slot < 40 and sudokuArray[slot] != 0:
			topCount += 1
		elif slot > 40 and sudokuArray[slot] != 0:
			bottomCount += 1
	#sets the program to begin either from the first slot and move down or last slot and move up
	sideOperator = 0
	#current index of the array
	slot = 0
	if topCount >= bottomCount:
		slot = 0
		sideOperator = 1
	else:
		slot = 80
		sideOperator = -1

	#stores solved puzzle so sudoku array can be used to check for multiple solutions
	solvedPuzzle = []
	#counts number of valid solutions
	numberOfSolutions = 0
	#will hold tuple of slot and previously tried number
	previousAltered = []
	#boolean to know if made a mistake and need to backtrack
	goBack = True
	#variable to track where trial numbers should begin from, important when backtracking
	currentStart = 1
	#while program is unfinished checks for both direction base case end
	while slot < 81 and slot >=0:
		#if the current slot is blank
		if sudokuArray[slot] == 0:
			#try to fit in a number between the current start and 9 inclusive
			for i in xrange(currentStart,10):
				#checks the trial number to see if it passes the three sudoku critera
				if checkValidNumber(sudokuArray, i, slot):
					#if it passes then it is inserted into the array
					sudokuArray[slot] = i
					#if there are no more blank cells
					if not 0 in sudokuArray:
						#increment number of solutions
						numberOfSolutions += 1
						#if first solution, make copy in solvedPuzzle and move on
						if numberOfSolutions == 1:
							solvedPuzzle = list(sudokuArray)
						#if more than 1 solution exits to main and reports problem
						elif numberOfSolutions >1:
							print "Puzzle Has More Than One Solution"
							exit()
						#program continues to look for solutions by backtracking
						sudokuArray[slot] = 0
					else:
						#the insertion is tracked by adding a tuple of the slot and number
						# to the previouslyAltered Array
						previousAltered.append((slot, i))
						#either 1 or -1 based on direction of solving
						slot += sideOperator
						currentStart=1
						#number found that fits, don't need to go back
						goBack = False
						#breaks out of the for loop to continue on
						break
			#if all numbers have been tried in this slot in the current configuration
			#then must go back and backtrack
			if goBack:
				#last holds the tuple of the most recent addition to the array
				if len(previousAltered)<=0:
					if numberOfSolutions ==1:
						print "Puzzle has a unique solution"
						return solvedPuzzle
					else: 
						#if there is already a solved puzzle then the puzzle was solved when given
						if not solvedPuzzle:
							print "Puzzle has no valid solution"
						exit()
				else:
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
			slot += sideOperator
	print "Puzzle Is Already Solved"
	return sudokuArray
 
#checks the trial entry in a particular slot to see if the rol, col, and box requirements are met
def checkValidNumber(sudokuArray, current, slot):
	#finds the column number of the current slot
	col = slot % 9
	#finds whether its the 1st 2nd or 3rd col or row in the square
	rowMod = (slot/9)%3
	colMod = col%3
	#finds the upper left slot of the square
	first = slot-colMod-(rowMod*9)
	#finds all of the slots that correspond the the same column
	for key in xrange(col, len(sudokuArray), 9):
		#checks the current against all numbers in the column
		if sudokuArray[key] == current:
			return False
	#finds all slots that correspond to the same row
	for key in xrange(slot-col, slot-col+9):
		#checks current against all numbers in the row
		if sudokuArray[key] == current:
			return False
	#checks square
	for i in xrange(0,3):
		for j in xrange(0,3):
			key = first+j+(i*9)
			if sudokuArray[key] == current:
				return False
	return True
 
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
 
if __name__ == "__main__":
    main()