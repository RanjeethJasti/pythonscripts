#!/usr/bin/python

#Basic authentication program


authdict = {'user1': 'user1@123', 'user2': 'user2@123', 'user3': 'user3@123'}

user = raw_input("Enter your username: ")
password = raw_input("Enter your password: ")

if authdict[user] == password:
	print "Authentication Success!"

else:
	print "Authentication Failure!"


