#!/usr/bin/python

# Fibonacci numbers module

def fib(n): # return Fibonacci series up to n
    """fibanocci series upto n 	
       Usage: fib(n)"""
    result = [0]
    a, b = 0, 1
    while b < n:	
        result.append(b)
        a, b = b, a+b
    return result


if __name__ == '__main__':

   limit = input("Enter the range: ")
   print fib(limit)
   print fib(1000)
