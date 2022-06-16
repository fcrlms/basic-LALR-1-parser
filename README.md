# About
VERY basic implementation of LALR(1) parser for final course assignment

The code generates the parsing table for the given CFG (`grammar.txt`) and then
parses the given string (`input.txt`)

If the string belongs to the grammar, the rightmost derivation that produces that
string will be printed to the terminal

# Limitations
Doesn't accept left recursive grammars nor grammars
that have empty string productions (ε-productions)

# How to run
Modify `grammar.txt` and `input.txt` to your liking then
run using python: `python3 ./main.py`

# How input works
## Grammar
The CFG goes in `grammar.txt`

Every CFG must have a starting S0 rule

All rules must conform to this format:
```
A : B | c D | E f | g H i | j
```
`A` is the nonterminal that originates the rule and the symbols in each production
MUST be separated by whitespace

## Input string
The input string goes in `string.txt`

All whitespaces will be ignored by the parser, so the input:
```
1 2 3 * 4 5 6 + 9
```
Would be parsed as:
```
123*456+90
```

## Examples
Examples of grammar and input strings are available in the folder `examples/`
