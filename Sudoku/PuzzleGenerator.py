#generates a random sudoku puzzle

import random

class PuzzleGenerator():
	sudokuArray = [0]*81
	possibleEntries = [0]*81

	def generatePuzzle(self):
		for x in range(0,81):
			self.possibleEntries[x]=range(1,10)
		slot = 0
		while slot < len(self.sudokuArray):
			#random number from possible entries
			if (len(self.possibleEntries[slot]) > 0):
				current = self.possibleEntries[slot][random.randrange(0,len(self.possibleEntries[slot]))]
				if self.checkValidNumber(current,slot):
					self.sudokuArray[slot]=current
					slot += 1
				else:
					self.possibleEntries[slot].remove(current)
			else:
				self.possibleEntries[slot]=range(1,10)
				slot -= 1
				current = self.sudokuArray[slot]
				self.possibleEntries[slot].remove(current)
				self.sudokuArray[slot] = 0
		self.printResult()
		return self.sudokuArray

	#checks the trial entry in a particular slot to see if the col crieteria is passed
	def checkValidNumber(self, current, slot):
		#finds the column number of the current slot
		col = slot % 9
		row = slot/9
		#finds whether its the 1st 2nd or 3rd col or row in the square
		rowMod = row%3
		colMod = col%3
		#finds the upper left slot of the square
		first = slot-colMod-(rowMod*9)
		#finds all of the slots that correspond the the same column
		for key in range(col, len(self.sudokuArray), 9):
			#checks the current against all numbers in the column
			if self.sudokuArray[key] == current:
				return False
				#finds all slots that correspond to the same row
		for key in range(slot-col, slot-col+9):
			#checks current against all numbers in the row
			if self.sudokuArray[key] == current:
				return False
		#checks square
		for i in range(0,3):
			for j in range(0,3):
				key = first+j+(i*9)
				if self.sudokuArray[key] == current:
					return False
		return True

	def printResult(self):
		line = ""
		counter = 0
		for i in self.sudokuArray:
			if counter <9:
				line = line + str(i)
				counter +=1
			else:
				print line
				line = str(i)
				counter = 1
		print line