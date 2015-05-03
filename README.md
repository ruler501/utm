# Universal Turing Machine

Compiles a given program (with a still being determined syntax)
down to a Turing machine with the syntax of [Turing Machine Simulator](https://martinugarte.com/turingmachine/)

##Syntax of the Input
on each line you can do one of 6 things, you can loop, increment a variable, decrement a variable, pop a digit, change the most significant 0 to a 1, or create a copy of a variable

Variables are local to the block(loop), they are deleted upon exit and can then be reused/resized. i is a reserved variable for the input on the tape

###While loop:
	while i decr {
		...
	}
Means while i does not overflow subtract one then do the block. Same for increment. Both flip the bits when done(incr end with all 0's decr all 1's). 
For pop it is when it runs out of digits to remove, and for first it is when the number is all one's. Can be nested arbitrarily deep

###Increment:
	incr(i) 
adds 1 to i

###Decrement:
	decr(i)
subtracts 1 from i

###Pop:
    pop(i)
removes the least significant bit from i

###First:
    first(i)
changes the most significant 0 in i to a 1

###Assignment:
	a = i
creates a new variable a equal to i, you can assign to an existing variable, just don't overrun it's length which would cause undefined behavior

###Assignment with Allocation
	a = i,5
creates a new variable a equal to i, with 5 extra bits. If you assign a variable to itself it is zeroed out. Should only be used on the last variable declared,
otherwise will overrun length causing undefined behavior

###Assignment of a Constant
    a = 35,6
Creates a new variable a equal to 35%(2**6), in 6 bits, can be assigned to an existing variable, but again be careful to mind the length

##Syntax of the Output
    [current_state],[current_symbol]
    [new_state],[new_symbol], [> or < or -]

##Example
Multiplication.utm multiplies i(the original variable on the tape) by 5 and stores it in b

Subtraction.utm subtracts 5 from i

Length.utm calculates the length of i

FractionalMultiplication.utm multiplies i(as if all it's digits came after a decimal place) by .111

Division.utm still a work in progress, uses Newton's method to calculate 1/3 to the precision asked for with i