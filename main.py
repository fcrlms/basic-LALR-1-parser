from classes import RuleClass, TransitionClass, RuleGroupClass, IterClass
from parseInput import readGrammarDescription
import utils
from parser import createActionTable, createGotoTable, parse

# reads grammar from input
grammarDescription = readGrammarDescription("./grammar.txt")

# gets terminals and nonterminals
(terminals, nonterminals) = utils.parseSymbols(grammarDescription)

# program ends if grammar is invalid
utils.isGrammarValid(grammarDescription, nonterminals)

# detect and remove unreachable rules
utils.removeUnreachableRules(grammarDescription, nonterminals)

# create FIRST set
FIRST: dict = utils.genSetFIRST(grammarDescription, terminals)

# used for the SOLE PURPOSE of indexing the rules
grammarRules: list = utils.getGrammarRules(grammarDescription, terminals, nonterminals)

# creates initial state of our finite automata that describes the provided grammar
initialGroup: RuleGroupClass = utils.generateInitialTable(grammarDescription, grammarRules, terminals, nonterminals, FIRST)

# stores all states of our automata
ruleGroupList = [ initialGroup ]

# stores all transitions between states
transitionList: list = []

# creating new states from current state until the automata is done
i = 0
while i < len(ruleGroupList):
	# will index what symbols will be used in transitions and what
	# rules will be carried through the transition with that symbol
	possibleTransitionSymbols: dict = {}
	for s in terminals:
		possibleTransitionSymbols[s] = []
	for s in nonterminals:
		possibleTransitionSymbols[s] = []

	currRuleGroup = ruleGroupList[i]

	# assign rules to correct symbols in possibleTransitionSymbols
	for rule in currRuleGroup.rules:
		# cursor is at end and doesn't expect to read anything
		if rule.hasRecognized():
			continue

		expectedSymbol = rule.expecting()
		possibleTransitionSymbols[expectedSymbol].append(rule)

	for transitionSymbol, rules in possibleTransitionSymbols.items():
		if len(rules) == 0:
			continue

		candidateGroup = RuleGroupClass()

		for r in rules:
			# these rules have recognized transitionSymbol so we increment the cursor
			newRule = RuleClass(r.id, r.symbol, r.production, r.cursor+1, r.lookAheads)
			candidateGroup.addRule(newRule)

		# if any of these rules is expecting a nonterminal we need to add to the group the rules this
		# nonterminal produces
		utils.fillWithRemainingRules(grammarDescription, grammarRules, candidateGroup, nonterminals, FIRST)

		# check if candidateGroup already exists in table
		# if it does, create a transition to the existing group
		# if not, create the group and add a transition
		groupIndex = -1
		for j in range(len(ruleGroupList)):
			otherGroup = ruleGroupList[j]

			if candidateGroup == otherGroup:
				groupIndex = j
				break # found duplicate, exit for

		# candidateGroup is new, add it to the list
		if groupIndex == -1:
			ruleGroupList.append(candidateGroup)
			groupIndex = len(ruleGroupList) -1

		newTransition = TransitionClass(transitionSymbol, i, groupIndex)
		transitionList.append(newTransition)

	i += 1

# construction of parser tables
actionTuple = createActionTable(ruleGroupList, transitionList, terminals)
gotoTuple = createGotoTable(len(ruleGroupList), transitionList, nonterminals)

data = ""
try:
	with open("./input.txt", "r") as f:
		data = f.read().splitlines()[0]
except OSError as e:
	print(e)
	exit()

# ignoring whitespace
inputChain = [c for c in data if c != " "]
iterator = IterClass(inputChain)

print("Input:")
print("".join(inputChain))
print()

output: list = parse(iterator, grammarRules, actionTuple, gotoTuple)

def getRightMostNonTerminal (arr):
	i = len(arr) -1
	for char in reversed(arr):
		if char in nonterminals:
			return (i, char)
		i -= 1

	return (-1, None)

def replace (arr, i, elements):
	for e in elements:
		arr.insert(i, e)
		i += 1

	arr.pop(i)

# Producing rightmost derivation of input
sequence = [ ["S0"] ]
while len(output):
	curr = int(output.pop())

	currSeq = sequence[-1].copy()

	(i, c) = getRightMostNonTerminal(currSeq)

	prod = grammarRules[curr].production

	replace(currSeq, i, prod)

	sequence.append(currSeq)

print("\nRightmost derivation:")
for s in sequence:
	print(" ".join(s))
