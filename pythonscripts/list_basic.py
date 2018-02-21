#!/usr/bin/python
namelist = [ 'abcd', 786 , 2.23, 'john', 70.2 ]
tinynamelist = [123, 'john']

print (namelist)          # Prints complete namelist
print (namelist[0])       # Prints first element of the namelist
print (namelist[1:3])     # Prints elements starting from 2nd till 3rd 
print (namelist[2:])      # Prints elements starting from 3rd element
print (tinynamelist * 2)  # Prints namelist two times
print (namelist + tinynamelist) # Prints concatenated namelists
