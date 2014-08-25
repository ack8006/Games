#generates a random sudoku puzzle



#****to Check
#which functions need self
#implement find possibilities in unique solution

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
		#finds whether its the 1st 2nd or 3rd col or row in the square
		rowMod = (slot/9)%3
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
		#checks square 
		for i in xrange(0,3):
			for j in xrange(0,3):
				key = first+j+(i*9)
				if sudokuArrayCopy[key] == current:
					return False
		return True

	#************no longer Alters the Main Puzzle!!!!
	def uniqueSolution(self, sudokuArrayCopy):
		#for speed will start in the most crowded half of the puzzle 
		topCount = 0
		bottomCount = 0
		slot = 0
		for slot in xrange(0,80):
			if slot < 40 and sudokuArrayCopy[slot] != 0:
				topCount += 1
			elif slot > 40 and sudokuArrayCopy[slot] != 0:
				bottomCount += 1

		sideOperator = 0
		if topCount >= bottomCount:
			slot = 0
			sideOperator = 1
		else:
			slot = 80
			sideOperator = -1

		#counts number of valid solutions
		numberOfSolutions = 0
		#will hold tuple of slot and previously tried number
		previousAltered = []
		#boolean to know if made a mistake and need to backtrack
		goBack = True
		#variable to track where trial numbers should begin from, important when backtracking
		currentStart = 1
		#while program is unfinished
		while slot < 81 and slot >=0:
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
				slot +=sideOperator
		return numberOfSolutions

	def randomizeDigGlobally(self):
		#while count less than x?
		failureCount = 0
		while failureCount < 3:
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

	def jumpOneSlot(self, oddEven):
		print "Jump One Slot"
		slot = oddEven
		while slot < 81:
			if self.sudokuArray[slot] != 0:
				startTime = time.time()
				self.digHoles([slot])
				#self.printResult()
				#print ""
				print "Solve Time: " + str(time.time()-startTime)
			slot += 2
		self.puzzleStatistics()	

	def leftToRightTopToBottomDig(self):
		slot = 0
		print "0"
		while slot < 81:
			print "1"
			if self.sudokuArray[slot] != 0:
				startTime = time.time()
				self.digHoles([slot])
				#self.printResult()
				#print ""
				print "Solve Time: " + str(time.time()-startTime)
			slot += 1
		self.puzzleStatistics()

	def digHoles(self, slotList):
		previousAltered = []
		for slot in slotList:
			previousAltered.append((slot, self.sudokuArray[slot]))
			self.sudokuArray[slot] = 0
		sudokuArrayCopy = list(self.sudokuArray)
		print "to check: " 
		self.printResult()
		if self.uniqueSolution(sudokuArrayCopy) == 1:
			return True
		else:
			for item in previousAltered:
				self.sudokuArray[item[0]] = item[1]
			return False

#Time to Grade the Puzzle
#Order of Operations
#Easy (Show Possibilities, Hidden Singles, Naked Pairs/Triples, Hidden Pairs/Triples,
	#Naked Quads, Pointing Pairs, Box-Line Reduction)
#Tough (X-Wing, Simple Coloring, Y-Wing, SwordFish, XYZ Wing)
#Diabolical (X-Cycles, XY-Chain, 3D Medusa, Jelly-Fish, Uniq Rect, Ext Uniq Rect,
	#Hidden Unique Rect,WXYZ Wing, Aligned Pair Exclusion)
#Evil Redic
	
	def findDifficulty(self, sudokuArrayCopy):
		startTime = time.time()
		slotPossibilities = [range(1,10) for x in range(0,81)]
		print self.difficultyOrderOfOperations(sudokuArrayCopy, slotPossibilities)
		print "findDifficulty Time: " + str(time.time()-startTime)

		
	#****************debating whether or not to pursue this method recursively or with
	#a loop.  thinking a loop as i will be able to avoid passing the difficultly level

	def difficultyOrderOfOperations(self, sudokuArrayCopy, slotPossibilities):	
		#*************should implement scoring to determine true difficulty here
		print sudokuArrayCopy
		print " "
		#0 if fails, 1 if easy, 2 if med...
		highestDifficulty = 0
		slotPossibilities = self.findPossibilities(sudokuArrayCopy, slotPossibilities)
		#**be able to handle case where this solver doesn't find solution

		#*
		count = 0
		#** remove and count < 10
		while slotPossibilities.count([]) != len(slotPossibilities) and count < 10:
			print "difficultyLoop"
			#DIFFICULTY LEVEL 0 SOLUTIONS
			#slotPossibliites
			result = self.showPossibilities(sudokuArrayCopy, slotPossibilities)
			if result[0] == True:
				sudokuArrayCopy = result[1]
				slotPossibilities = self.findPossibilities(sudokuArrayCopy, slotPossibilities)
				count = 0
				continue

			#DIFFICULTY LEVEL 1 SOLUTIONS
			print "level 1"

			result = self.hiddenSingles(sudokuArrayCopy, slotPossibilities)
			if result[0] == True:
				sudokuArrayCopy = result[1]
				highestDifficulty = 1
				slotPossibilities = self.findPossibilities(sudokuArrayCopy, slotPossibilities)
				count = 0
				continue

			result = self.nakedDouble(slotPossibilities)
			if result[0] == True:
				highestDifficulty = 1
				slotPossibilities = result[1]
				count = 0
				continue

			count +=1
		print "****************FAILURE OVERCOUNT: " +str(count)

		#*****
		line = ""
		for x in sudokuArrayCopy:
			line = line + str(x)
		print line
		return highestDifficulty


	#do this by going through on cells that have a number, remove as a possibility from all in
	#same col, row and square
	def findPossibilities(self, sudokuArrayCopy, slotPossibilities):
		#startTime = time.time()
		for slot in xrange(0,81):
			if sudokuArrayCopy[slot] != 0:
				slotPossibilities[slot] = []
				col = slot % 9
				rowMod = (slot/9)%3
				colMod = col%3
				for key in xrange(0,9):
					#check col
					if sudokuArrayCopy[slot] in slotPossibilities[col+(key*9)]:
						slotPossibilities[col+(key*9)].remove(sudokuArrayCopy[slot])
					#check row
					if sudokuArrayCopy[slot] in slotPossibilities[slot-col+key]:
						slotPossibilities[slot-col+key].remove(sudokuArrayCopy[slot])
					#checkSquare
					first = slot-colMod-(rowMod*9)
					if sudokuArrayCopy[slot] in slotPossibilities[first+(key%3)+((key/3*9))]:
						slotPossibilities[first+(key%3)+((key/3*9))].remove(sudokuArrayCopy[slot])
		#print "Possibility Time: " + str(time.time()-startTime)
		return slotPossibilities

	def showPossibilities(self, sudokuArrayCopy, slotPossibilities):
		print "showPossibilities"
		#monitors whether or not anything was changed
		flag = False
		for slot, possibility in enumerate(slotPossibilities):
			if len(possibility) == 1:
				flag = True
				sudokuArrayCopy[slot] = possibility[0]
		return [flag, sudokuArrayCopy]

	#*******Major Bugs
	#bug in appending and removing and appending signles need to just count	
	def hiddenSingles(self, sudokuArrayCopy, slotPossibilities):
		print "hiddenSingles"
		#have array of ones found and slot, if found second time remove
		flag = False
		for section in xrange(0,9):
			#occurances of a possibility
			colSingles = [0]*9
			rowSingles = [0]*9
			squareSingles = [0]*9
			#squares left to right then top to bottom
			first = (section%3)*3 + (section/3)*27

			for key in xrange(0,9):
				#column
				for possibility in slotPossibilities[section+(key*9)]:
					colSingles[possibility-1] = colSingles[possibility-1] + 1
				#row
				for possibility in slotPossibilities[(section*9) + key]:
					rowSingles[possibility-1] = rowSingles[possibility-1] + 1
				#squares left to right then top to bottom
				for possibility in slotPossibilities[first+(key%3)+((key/3*9))]:
					squareSingles[possibility-1] = squareSingles[possibility-1] + 1
			#****could make these lines a method and pass the slot as a parameter
			#if any possibility occurs once in the column
			if 1 in colSingles:
				flag = True
				possibilities =[i for i, x in enumerate(colSingles) if x == 1]
				for possibility in possibilities:
					for key in xrange(0,9):
						if possibility+1 in slotPossibilities[section+(key*9)]:
							sudokuArrayCopy[section+(key*9)] = possibility+1

			if 1 in rowSingles:
				flag = True
				possibilities =[i for i, x in enumerate(rowSingles) if x == 1]
				for possibility in possibilities:
					for key in xrange(0,9):
						if possibility+1 in slotPossibilities[(section*9) + key]:
							sudokuArrayCopy[(section*9) + key] = possibility+1

			if 1 in squareSingles:
				flag = True
				possibilities =[i for i, x in enumerate(squareSingles) if x == 1]
				for possibility in possibilities:
					for key in xrange(0,9):
						if possibility+1 in slotPossibilities[first+(key%3)+((key/3*9))]:
							sudokuArrayCopy[first+(key%3)+((key/3*9))] = possibility+1

		return [flag, sudokuArrayCopy]						

	#returns slot possibilities instead of sudoku
	def nakedDouble(self, slotPossibilities):
		#two cells in same group have 2possibilites, other can be removed
		print "nakedDouble"
		flag = False
		for x in xrange(0,81):
			#remove values from the below conditions
			col = False
			row = False
			square = False
			#check all others and see if matches col row and square
			if len(slotPossibilities[x]) == 2 and slotPossibilities.count(slotPossibilities[x]) > 1:
				#finds all locations of occurances of the current slot possiblity
				occurances = [i for i, val in enumerate(slotPossibilities) if val == slotPossibilities[x]]
				for occurance in occurances:
					if x != occurance:
						if x % 9 == occurance % 9:
							col = True
						if x/9 == occurance / 9:
							row = True
						if x-(x%3)-(((x/9)%3)*9) == occurance-(occurance%3)-(((occurance/9)%3)*9):
							square = True
			#**could be function
			if col:
				flag = True
				for key in xrange(0,9):
					if slotPossibilities[x] != slotPossibilities[(key*9)+(x%9)]:
						slotPossibilities[(key*9)+(x%9)] = list(set(slotPossibilities[(key*9)+(x%9)]) - set(slotPossibilities[x]))
						slotPossibilities[(key*9)+(x%9)].sort()
			if row:
				flag = True
				for key in xrange(0,9):
					if slotPossibilities[x] != slotPossibilities[(x/9)*9+key]:
						slotPossibilities[(x/9)*9+key] = list(set(slotPossibilities[(x/9)*9+key]) - set(slotPossibilities[x]))
						slotPossibilities[(x/9)*9+key].sort()
			if square:
				flag = True
				#finds the upper left slot of the square
				first = x-(x%3)-(((x/9)%3)*9)
				for key in xrange(0,9):
					if slotPossibilities[x] != slotPossibilities[first+(key%3)+((key/3*9))]:
						slotPossibilities[first+(key%3)+((key/3*9))] = list(set(slotPossibilities[first+(key%3)+((key/3*9))]) - set(slotPossibilities[x]))
						slotPossibilities[first+(key%3)+((key/3*9))].sort()

		return [flag, slotPossibilities]











	def hiddenDouble(self, slotPossibilities):
		pass











	def puzzleStatistics(self):
		self.printResult()
		count = 0
		for slot in self.sudokuArray:
			if slot != 0:
				count += 1
		print "Filled Values: " + str(count)
		print self.findDifficulty(list(self.sudokuArray))
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
#*****to remove
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

	randomizeCheck()
	#jumpOneSlotCheck()
	#leftToRightCheck()
	#jumpLeftCheck()
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
	sudokuArrayCopy = list(sudokuArray)
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

def jumpOneSlotCheck():
	PuzzleGen = PuzzleGenerator()
	sudokuArray = PuzzleGen.generateCompleted()
	PuzzleGen.jumpOneSlot(0)
	PuzzleGen.jumpOneSlot(1)

def jumpLeftCheck():
	PuzzleGen = PuzzleGenerator()
	sudokuArray = PuzzleGen.generateCompleted()
	PuzzleGen.jumpOneSlot(0)
	PuzzleGen.leftToRightTopToBottomDig()	

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











