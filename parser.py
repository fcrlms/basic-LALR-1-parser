from classes import IterClass
from utils import getRuleN, getRuleNSize

def createActionTable (ruleGroupList: list, transitionList: list, terminals: list) -> tuple:
	ActionIndex = {}

	columns = len(terminals)

	for i in range(columns):
		ActionIndex[terminals[i]] = i

	columns += 1
	ActionIndex["EOF"] = columns-1

	actionTable = []
	lines = len(ruleGroupList)

	# initialize table
	for i in range(lines):
		actionTable.append([])
		for j in range(columns):
			actionTable[i].append(None)


	# create reductions
	for i, group in enumerate(ruleGroupList):
		for r in group.rules:
			if not r.hasRecognized():
				continue

			if r.symbol == "S0":
				actionTable[i][ActionIndex["EOF"]] = "acc"
				continue

			# parser will only reduce rule when it
			# recognizes one of it's lookaheads
			for l in r.lookAheads:
				index = ActionIndex[l]
				actionTable[i][index] = f"r {r.id}"

	# create shifts
	for t in transitionList:
		if t.symbol not in terminals:
			continue

		# tells the parser to consume the symbol and
		# go to state 't.destination'
		index = ActionIndex[t.symbol]
		actionTable[t.origin][index] = f"s {t.destination}"

	return (actionTable, ActionIndex)

def createGotoTable (totalLines: int, transitionList: list, nonterminals: list) -> tuple:
	GotoIndex = {}

	# nonterminals minus S0
	columns = 0
	for symb in nonterminals:
		if symb == "S0":
			continue

		GotoIndex[symb] = columns
		columns += 1

	gotoTable = []

	# initialize table
	for i in range(totalLines):
		gotoTable.append([])

		for j in range(columns):
			gotoTable[i].append(None)

	# creating gotos
	for t in transitionList:
		if t.symbol not in nonterminals:
			continue

		# tells the parser to go from origin to destination
		# when the nonterminal 't.symbol' is recognized
		index = GotoIndex[t.symbol]
		gotoTable[t.origin][index] = t.destination

	return (gotoTable, GotoIndex)

def parse (iterator: IterClass, grammarRules: list, actionTuple: tuple, gotoTuple: tuple) -> list:
	(actionTable, ActionIndex) = actionTuple
	(gotoTable, GotoIndex) = gotoTuple

	# state stack
	stack = [ 0 ]

	# actual parser output
	output = []

	# id of recognized rule
	recog = -1

	while True:
		currChar = iterator.current()
		currState = stack[-1] # top of stack

		# if a rule has been recognized use goto table
		if recog >= 0:
			# the nonterminal that originates this rule
			symb = getRuleN(grammarRules, recog)

			# the number of symbols in the rules is the
			# amount of states we pop from the stack
			popTimes = getRuleNSize(grammarRules, recog)
			for i in range(popTimes):
				stack.pop()

			currState = stack[-1]

			index = GotoIndex[symb]
			newState = gotoTable[currState][index]

			if newState == None:
				print("[Denied] Input cannot be derived from given CFG")
				exit()

			stack.append(int(newState))

			# resets recognized rule
			recog = -1

		# use action table
		else:
			index = ActionIndex[currChar]
			res = actionTable[currState][index]

			if res == None:
				print("[Denied] Input cannot be derived from given CFG")
				exit()

			if res == "acc":
				print("[Accepted] Input belongs to given CFG")

				# add S0 production to derivation
				output.append(0)
				break

			(action, n) = res.split(" ")

			# shift to state n, consumes char
			if action == 's':
				iterator.consume()
				stack.append(int(n))

			# reduce to rule n, doesn't consume char
			elif action == 'r':
				output.append(n)
				recog = int(n)
			else:
				print("[Denied] Input cannot be derived from given CFG")
				exit()

	return output
