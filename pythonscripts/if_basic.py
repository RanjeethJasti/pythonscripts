#!/usr/bin/python

#Learning if condition

name = raw_input("Enter you name: ")
age = input("Enter you age: ")


if age < 5: 

   print "Hello %s.. You are an infant" % name

elif age < 18 :
   
   print "Hello %s.. You are an minor" % name

elif age < 60: 

   print "Hello %s.. You age is %d " % (name,age)
   print "Congrats..!"

else:
   print "Hello %s.. Your age is %d" % (name,age)

print "Bye"
