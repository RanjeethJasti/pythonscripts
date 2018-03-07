#!/usr/bin/python

import sys

# This is a program to check user authentication

username = raw_input("Enter your username: ")
password = raw_input("Password: ")
pattern  = None

fh = open("auth.txt", "r")

for line in fh.readlines():
    if username in line:
        pattern = line

if not pattern:
    print "User does not exits!"
    sys.exit(1)

auth_list = pattern.split(":")
if password in auth_list[1]:
    print "Authentication Granted"
else:
    print "Access denied!"
