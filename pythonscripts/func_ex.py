def add_func(a, b):

        """A function to add 3
        numbers"""
        x = a + b
        return(x)

def diff_func(a, b):

        """A function to substract 2 numbers"""
        x = a - b
        return(x)

def div_func(a, b):

	"""A function for dividing two numbers"""

	x = a / b
	return x




sum = add_func(10, 20)
print sum
print add_func(40, 50)
print "The difference is: " + str(diff_func(40,30))
print "division is: ",
print div_func(10, 2)
