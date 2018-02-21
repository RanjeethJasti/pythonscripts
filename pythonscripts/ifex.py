#!/usr/bin/python

balance_info = {'Joseph': 1000, 'John': -500, 'Ann': 0}
name = raw_input("Enter your name:")
#balance = balance_info[name]

if not balance_info.has_key(name):
    print "User %s does'nt exists.. " %(name)
    exit (0)
balance = balance_info[name]

if balance < 0:
    print("Balance is %d, add funds now or you will be charged a penalty.") %(balance)

elif balance == 0:
    	print("Balance is %d, add funds soon.") %(balance)

else:
    print("Your balance is %d") %(balance)
