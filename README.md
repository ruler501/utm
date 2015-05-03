# Universal Turing Machine

Compiles a given program (with a still being determined syntax)
down to a Turing machine with the syntax of [Turing Machine Simulator](https://martinugarte.com/turingmachine/)

##Syntax of the Input
on each line you can do one of 5 things, you can loop, increment a variable, decrement a variable, pop a digit, or create a copy of a variable

Variables are local to the block(loop), they are deleted upon exit and can then be reused/resized.

###While loop:
	while i decr {
		...
	}
Means while i does not overflow subtract one then do the block. For increment it is while i is not all ones. Both flip the bits when done(incr end with all 0's decr all 1's). Can only be nested two deep.

###Increment:
	incr(i) 
adds 1 to i

###Decrement:
	decr(i)
subtracts 1 from i

###Pop:
    pop(i)
removes a digit from i

###Assignment:
	a = i
creates a new variable a equal to i, you cannot assign to an existing variable you can assign to an existing variable, just don't overrun it's length, that causes undefined behavior

###Assignment with Allocation
	a = i,5
creates a new variable a equal to i, with 5 extra bits. If you assign a variable to itself it is zeroed out.

###Assignment of a Constant
    a = 35,6
Creates a new variable a equal to 35%(2**6), in 6 bits,

##Syntax of the Output
    [current_state],[current_symbol]
    [new_state],[new_symbol], [> or < or -]

##Example
Multiplication.utm multiplies i(the original variable on the tape) by 5 and stores it in b

Subtraction.utm subtracts 5 from i

