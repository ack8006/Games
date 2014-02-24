import sys
import fileinput
import os


def main():
	#will eventually have a stream reader to take directory, now hardcoded
	#sudokuFile = "test1.txt"
	sudokuFile = "tester.txt"

	#takes the file location and parses it into an array
	sudokuArray = parseFile(sudokuFile)
	print sudokuArray
	for key, val in enumerate(sudokuArray):
		print checkValidNumber(val, key, sudokuArray)

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
		if sudokuArray[key] == current and  key != slot:
			return False
			#finds all slots that correspond to the same row
	for key in range(slot-col, slot-col+9):
		#checks current against all numbers in the row
		if sudokuArray[key] == current and key != slot:
			return False
	#checks square
	for i in range(0,3):
		for j in range(0,3):
			key = first+j+(i*9)
			if sudokuArray[key] == current and key != slot:
				return False
	return True


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

if __name__ == "__main__":
    main()
