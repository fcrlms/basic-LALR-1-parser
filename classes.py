class RuleClass:
	def __init__ (self, id, symbol, production, cursor, lookAheads):
		self.id = id
		self.symbol = symbol
		self.production = production
		self.cursor = cursor

		if not isinstance(lookAheads, set):
			if isinstance(lookAheads, list):
				lookAheads = set(lookAheads)
			else:
				lookAheads = set([ lookAheads] )

		self.lookAheads = lookAheads

	def __eq__ (self, other):
		if (isinstance(other, RuleClass)):
			equalSymbol = self.symbol == other.symbol
			equalProd = self.production == other.production
			equalCursor = self.cursor == other.cursor
			equalLookAheads = self.lookAheads == other.lookAheads
			return equalSymbol and equalProd and equalCursor and equalLookAheads
		else:
			return False

	def prettyPrint (self, cursor=True):
		# use a copy to avoid modifying original prodution list
		prod = self.production.copy()

		# print cursor
		if cursor:
			if (self.cursor >= len(prod)):
				prod.append(".")
			else:
				prod[self.cursor] = "." + prod[self.cursor]

		prod = ''.join(prod)

		return f"({self.id}) {self.symbol} -> {prod}\t\t{self.lookAheads}"

	# returns the production symbol this rule is currently expecting to read
	def expecting (self):
		if (self.cursor >= len(self.production)):
			pass
		else:
			return self.production[self.cursor]

	def nextExpected (self):
		if not self.expecting():
			return None

		if (self.cursor +1 >= len(self.production)):
			return None

		return self.production[self.cursor +1]

	# returns true if the cursor is at the end of the production
	# i.e.: the rule has been recognized
	def hasRecognized (self):
		return self.cursor >= len(self.production)

	# similar is same symbol, same prod and same cursor
	# used to detect similar rules when merging lookAheads
	def isSimilarTo (self, other):
		sameSymbol = self.symbol == other.symbol
		sameProd = self.production == other.production
		sameCursor = self.cursor == other.cursor

		return sameSymbol and sameProd and sameCursor

class RuleGroupClass:
	def __init__ (self):
		self.rules = []
		return

	def __eq__ (self, other):
		if (isinstance(other, RuleGroupClass)):
			cloneSelf = self.rules.copy()
			cloneOther = other.rules.copy()

			try:
				for c in cloneSelf:
					index = cloneOther.index(c)
					cloneOther.pop(index)
			except ValueError:
				return False

			return len(cloneOther) == 0
		else:
			return False

	def addRule (self, rule):
		if (not isinstance(rule, RuleClass)):
			raise TypeError()

		if rule in self.rules:
			return

		self.rules.append(rule)


# class that represents a transition from one state to another
class TransitionClass:
	def __init__ (self, symbol, origin, destination):
		self.symbol = symbol
		self.origin = origin
		self.destination = destination

# used by the parser to read input
class IterClass:
	def __init__ (self, chain: list):
		self.chain = chain
		self.currIndex = 0

	def consume (self) -> None:
		self.currIndex += 1

	def current (self) -> str:
		if self.currIndex >= len(self.chain):
			return "EOF"
		else:
			return self.chain[self.currIndex]
