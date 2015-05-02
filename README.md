# Universal Turing Machine

Compiles a given program (with a still being determined syntax)
down to a Turing machine with the syntax of [Turing Machine Simulator](https://martinugarte.com/turingmachine/)

##Syntax of the Input
on each line you can do one of 4 things, you can loop, increment a variable, decrement a variable or create a copy of a variable

###While loop:
	while i decr {
		...
	}
Means while i is not all zero's subtract one then do the block. For increment it is while i is not all ones. Both flip the bits when done(incr end with all 0's decr all 1's)

###Increment:
	incr(i) 
adds 1 to i

###Decrement:
	decr(i)
subtracts 1 from i

###Assignment:
	a = i
creates a new variable a equal to i, you cannot assign to an existing variable.

###Assignment with Allocation
	a = i,5
creates a new variable a equal to i, with 5 extra bits.

##Syntax of the Output
[current_state],[current_symbol]
[new_state],[new_symbol], [> or < or -]

##Example
For a working example see UTM.utm in this repository