#generates a random sudoku puzzle

import random
import time
import cProfile

class PuzzleGenerator():
	sudokuArray = [0]*81

	def generateCompleted(self):
		possibleEntries = [0]*81
		for x in xrange(0,81):
			possibleEntries[x]=list(xrange(1,10))
		slot = 0
		while slot < 81:
			#random number from possible entries
			if (len(possibleEntries[slot]) > 0):
				current = possibleEntries[slot][random.randrange(0,len(possibleEntries[slot]))]
				if self.checkValidNumber(current,slot, self.sudokuArray):
					self.sudokuArray[slot]=current
					slot += 1
				else:
					possibleEntries[slot].remove(current)
			else:
				possibleEntries[slot]=list(xrange(1,10))
				slot -= 1
				current = self.sudokuArray[slot]
				possibleEntries[slot].remove(current)
				self.sudokuArray[slot] = 0
		self.printResult()
		return self.sudokuArray

	#checks the trial entry in a particular slot to see if the rol, col, and box requirements are met
	def checkValidNumber(self, current, slot, sudokuArrayCopy):
		#finds the column number of the current slot
		col = slot % 9
		row = slot/9
		#finds whether its the 1st 2nd or 3rd col or row in the square
		rowMod = row%3
		colMod = col%3
		#finds the upper left slot of the square
		first = slot-colMod-(rowMod*9)
		#finds all of the slots that correspond the the same column
		for key in xrange(col, 81, 9):
			#checks the current against all numbers in the column
			if sudokuArrayCopy[key] == current:
				return False
		#finds all slots that correspond to the same row
		for key in xrange(slot-col, slot-col+9):
			#checks current against all numbers in the row
			if sudokuArrayCopy[key] == current:
				return False
		#checks square lower 4 square
		for i in xrange(0,3):
			for j in xrange(0,3):
				key = first+j+(i*9)
				if sudokuArrayCopy[key] == current:
					return False
		return True

	#************no longer Alters the Main Puzzle!!!!
	def uniqueSolution(self, sudokuArrayCopy):
		#counts number of valid solutions
		numberOfSolutions = 0
		#current index of array
		slot = 0 
		#will hold tuple of slot and previously tried number
		previousAltered = []
		#boolean to know if made a mistake and need to backtrack
		goBack = True
		#variable to track where trial numbers should begin from, important when backtracking
		currentStart = 1
		#while program is unfinished
		while slot < 81:
			#if the current slot is blank
			if sudokuArrayCopy[slot] == 0:
				#try to fit in a number between the current start and 9 inclusive
				for i in xrange(currentStart,10):
					#checks the trial number to see if it passes the three sudoku critera
					if self.checkValidNumber(i, slot, sudokuArrayCopy):
						#if it passes then it is inserted into the array
						sudokuArrayCopy[slot] = i
						if not 0 in sudokuArrayCopy:
							numberOfSolutions += 1
							if numberOfSolutions >1:
								#**********trial 
								sudokuArrayCopy = []
								return numberOfSolutions
							sudokuArrayCopy[slot] = 0
						else:
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
					if len(previousAltered)<=0:
						#**********trial 
						sudokuArrayCopy = []
						return numberOfSolutions
					else:
						last = previousAltered.pop()
						#sets slot to the previously altered slot and set current start to 
						#one more than the number that was most recently tried in that slot
						slot = last[0]
						currentStart = last[1]+1
						#resets slot to zero
						sudokuArrayCopy[slot] = 0
				#if goBack is False, it's reset to true and the loop continues
				else: goBack = True
			#if the current slot is not zero go to the next slot
			else:
				slot +=1
		return numberOfSolutions

	def randomizeDigGlobally(self):
		#while count less than x?
		failureCount = 0
		while failureCount < 1:
			slot = random.randrange(0,80)
			if self.sudokuArray[slot] != 0:
				if not self.digHoles([slot]):
					failureCount += 1
				else:
					failureCount = 0
			print "failures: " + str(failureCount)
			self.printResult()
			print " "
		self.puzzleStatistics()

	#symmetrical
	#def randomizeDigGlobally(self):
	#	#while count less than 5?
	#	failureCount = 0
	#	while failureCount < 4:
	#		slot = random.randrange(0,41)
	#		if self.sudokuArray[slot] != 0:
	#			#handle 40 double
	#			slotList = []
	#			if slot == 40:
	#				slotList = [slot]
	#			else:
	#				slotList = [slot, 80-slot]
	#			if not self.digHoles(slotList):
	#				failureCount += 1
	#			else:
	#				failureCount = 0
	#		print failureCount
	#		self.printResult()
	#		print " "
	#	self.puzzleStatistics()

	def leftToRightTopToBottomDig(self):
		slot = 80
		print "0"
		while slot >= 0:
			print "1"
			if self.sudokuArray[slot] != 0:
				startTime = time.time()
				print "not 0"
				self.digHoles([slot])
				#self.printResult()
				#print ""
				print "Solve Time: " + str(time.time()-startTime)
			slot -= 1
		self.puzzleStatistics()

	#SYMMETRICAL
	#def leftToRightTopToBottomDig(self):
	#	slot = random.randrange(0,41)
	#	count = 0
	#	while count <= 40:
	#		slotList = []
	#		if slot == 40:
	#			slotList = [slot]
	#		else:
	#			slotList = [slot, 80-slot]
	#		self.digHoles(slotList)
	#		slot += 1
	#		count += 1
	#		self.printResult()
	#		print ""
	#	self.puzzleStatistics()

	def digHoles(self, slotList):
		previousAltered = []
		for slot in slotList:
			previousAltered.append((slot, self.sudokuArray[slot]))
			self.sudokuArray[slot] = 0
		sudokuArrayCopy = []
		for number in self.sudokuArray:
			sudokuArrayCopy.append(number)
		print "to check: " 
		self.printResult()
		if self.uniqueSolution(sudokuArrayCopy) == 1:
			return True
		else:
			for item in previousAltered:
				self.sudokuArray[item[0]] = item[1]
			return False

	
	def puzzleStatistics(self):
		self.printResult()
		count = 0
		for slot in self.sudokuArray:
			if slot != 0:
				count += 1
		print "Filled Values: " + str(count)
		#boxes
		#row, col = 0
		#while row <3:
		#	while col < 3:
		#		box = [0,1,2,9,10,11,18,19,20]

	def printResult(self):
		line = ""
		counter = 0
		for i in self.sudokuArray:
			#if counter <9:
			line = line + str(i)
			counter +=1
			#else:
			#	print line
			#	line = str(i)
			#	counter = 1
		print line

#random tests
	def tester(self, sudokuArrayCopy):
		sudokuArrayCopy[0]="a"
		print self.sudokuArray
		print sudokuArrayCopy


def main():
	#x = PuzzleGenerator()
	startTime = time.time()
	#x.generateCompleted()
	#print "Solve Time: " + str(time.time()-startTime)
	
	#Unit Tests
	#singleSolutionCheck()
	#multipleSolutionCheck()
	#digHolesCheck()
	#testCase()

	#randomizeCheck()
	leftToRightCheck()
	#randomLeft()

	print "Solve Time: " + str(time.time()-startTime)

#Various Unit Tests

#random tests
def testCase():
	PuzzleGen = PuzzleGenerator()
	PuzzleGen.tester(PuzzleGen.sudokuArray)

def singleSolutionCheck():
	PuzzleGen = PuzzleGenerator()
	startTime = time.time()
	sudokuArray = PuzzleGen.generateCompleted()
	print "Puzzle Gen Time: " + str(time.time()-startTime)
	for slot in xrange(0,81):
		if sudokuArray[slot] == 1:
			sudokuArray[slot] = 0
	PuzzleGen.sudokuArray = sudokuArray
	PuzzleGen.uniqueSolution()

#***Fails Now
def multipleSolutionCheck():
	PuzzleGen = PuzzleGenerator()
	startTime = time.time()
	sudokuArray = PuzzleGen.generateCompleted()
	print "Puzzle Gen Time: " + str(time.time()-startTime)
	for slot in xrange(0,81):
		if sudokuArray[slot] == 1 or sudokuArray[slot] == 2 or sudokuArray[slot] == 4:
			sudokuArray[slot] = 0
	print PuzzleGen.uniqueSolution(sudokuArray)	

def digHolesCheck():
	PuzzleGen = PuzzleGenerator()
	sudokuArray = PuzzleGen.generateCompleted()
	sudokuArrayCopy = []
	for number in sudokuArray:
		sudokuArrayCopy.append(number)
	for x in xrange(0,80,2):
		mult = PuzzleGen.digHoles([x, x+1], sudokuArrayCopy)
		print mult
		if mult:
			print PuzzleGen.printResult()
			print " "
		else:
			print PuzzleGen.printResult()
			print " "
			break

def randomizeCheck():
	PuzzleGen = PuzzleGenerator()
	sudokuArray = PuzzleGen.generateCompleted()
	PuzzleGen.randomizeDigGlobally()

def leftToRightCheck():
	PuzzleGen = PuzzleGenerator()
	sudokuArray = PuzzleGen.generateCompleted()
	PuzzleGen.leftToRightTopToBottomDig()

def randomLeft():
	PuzzleGen = PuzzleGenerator()
	sudokuArray = PuzzleGen.generateCompleted()
	PuzzleGen.randomizeDigGlobally()
	PuzzleGen.leftToRightTopToBottomDig()	


if __name__ == "__main__":
    main()











