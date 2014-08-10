#generates a random sudoku puzzle

import random
import time
import cProfile

class PuzzleGenerator():
	sudokuArray = [0]*81
	possibleEntries = [0]*81

	def generateCompleted(self):
		for x in range(0,81):
			self.possibleEntries[x]=range(1,10)
		slot = 0
		while slot < len(self.sudokuArray):
			#random number from possible entries
			if (len(self.possibleEntries[slot]) > 0):
				current = self.possibleEntries[slot][random.randrange(0,len(self.possibleEntries[slot]))]
				if self.checkValidNumber(current,slot, self.sudokuArray):
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

	#1 is easy, 2 medium, 3 hard, 4 very hard
	#easy >32, 30-32,28-30,<28
	#>1 each box, couple with only one given, """", several with no givens
	#each digit appears at least 3 times, some may only appear twice, 3-4 appear twice 1 once, 
	#several single digit and most 2-3
	#http://alwayspuzzling.blogspot.com/2012/12/how-to-judge-difficulty-of-sudoku.html
	#def difficultyGenerator(self, difficulty):
	#	#copy array
	#	sudokuArrayCopy = []
	#	for slot in self.sudokuArray:
	#		sudokuArrayCopy.append(slot)

	def randomizeDigGlobally(self):
		#while count less than x?
		failureCount = 0
		while failureCount < 2:
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
	#	while failureCount < 1000:
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
		slot = 0
		while slot <= 80:
			self.digHoles([slot])
			slot += 1
			#self.printResult()
			#print ""
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
		for key in range(col, len(self.sudokuArray), 9):
			#checks the current against all numbers in the column
			if sudokuArrayCopy[key] == current:
				return False
		#finds all slots that correspond to the same row
		for key in range(slot-col, slot-col+9):
			#checks current against all numbers in the row
			if sudokuArrayCopy[key] == current:
				return False
		#checks square
		for i in range(0,3):
			for j in range(0,3):
				key = first+j+(i*9)
				if self.sudokuArray[key] == current:
					return False
		return True

	#************ Do I need to return solutions or should i just return if greater than 2?
	#************ Probably Just if Greater than 2 because I'm no going to need the actual solutions
	#and it will be much faster to run if only looking for 2

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
		while slot < len(sudokuArrayCopy):
			#if the current slot is blank
			if sudokuArrayCopy[slot] == 0:
				#try to fit in a number between the current start and 9 inclusive
				for i in range(currentStart,10):
					#checks the trial number to see if it passes the three sudoku critera
					if self.checkValidNumber(i, slot, sudokuArrayCopy):
						#if it passes then it is inserted into the array
						sudokuArrayCopy[slot] = i
						if not 0 in sudokuArrayCopy:
							numberOfSolutions += 1
							if numberOfSolutions >1:
								print "checkOver1"
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
						print "check1"
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
		print "check3"
		return numberOfSolutions

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
	startTime = time.time()
	#singleSolutionCheck()
	#multipleSolutionCheck()
	#multipleSolutionCheck2()
	#digHolesCheck()
	#testCase()

	randomizeCheck()
	#leftToRightCheck()
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
	for slot in range(0,81):
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
	for slot in range(0,81):
		if sudokuArray[slot] == 1 or sudokuArray[slot] == 2 or sudokuArray[slot] == 4:
			sudokuArray[slot] = 0
	print PuzzleGen.uniqueSolution(sudokuArray)	

#****
def multipleSolutionCheck2():
	PuzzleGen = PuzzleGenerator()
	startTime = time.time()
	puzzle = "420001093053720800861503704508309072040100938700286401370608240100970065296435107"
	sudokuArray = []
	while len(puzzle) >0:
		sudokuArray.append(int(puzzle[0]))
		puzzle = puzzle[1:]
	print sudokuArray
	PuzzleGen.sudokuArray = sudokuArray
	print PuzzleGen.uniqueSolution(sudokuArray)

def digHolesCheck():
	PuzzleGen = PuzzleGenerator()
	sudokuArray = PuzzleGen.generateCompleted()
	sudokuArrayCopy = []
	for number in sudokuArray:
		sudokuArrayCopy.append(number)
	for x in range(0,80,2):
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











