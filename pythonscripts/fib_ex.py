def fib(n): # return Fibonacci series up to n
    
    """fibanocci series upto n 
        Usage: fib(n)"""

    result = [0]
    a, b = 0, 1
    while b < n:
        result.append(b)
        a, b = b, a+b
    return result


