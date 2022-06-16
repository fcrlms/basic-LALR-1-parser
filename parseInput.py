from classes import RuleClass

def isValidSymbol (symb: str) -> bool:
	if len(symb.split()) > 1:
		return False

	return True

def isValidProduction (symbol: str, productions: list) -> bool:
	for prod in productions:
		# empty production
		if len(prod) == 0:
			return False

		# Only Leads to itself (recursive)
		if len(prod) == 1 and prod[0] == symbol:
			return False

	return True

def readGrammarDescription (grammarFile: str) -> dict:
	lines = ""
	try:
		with open(grammarFile, mode="r") as f:
			lines = f.read().splitlines()
	except OSError as e:
		print(e)
		exit()

	grammar = {}

	for i, line in enumerate(lines):
		# ignore empty lines
		if line == '':
			continue

		split = [c.strip() for c in line.split(":", 1)]

		# rule must be of format:
		# nonterminal : AnyCombinationOfTerminalsAndNonterminals
		if len(split) < 2:
			print(f"[Error: line {i+1}] Invalid rule!")
			exit()

		(symbol, productions) = split

		# symbol must be chain of letters without whitespace between them
		if not isValidSymbol(symbol):
			print(f"[Error: line {i+1}] '{symbol}' is not a valid symbol!")
			exit()

		productions = [p.split() for p in productions.split("|")]

		# empty and recursive productions are invalid
		if not isValidProduction(symbol, productions):
			print(f"[Error: line {i+1}] Invalid production!")
			exit()

		grammar[symbol] = productions

	return grammar
