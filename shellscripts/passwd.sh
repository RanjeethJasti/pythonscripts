#!/bin/bash
# This is some secure program that uses security.

VALID_PASSWORD="secret" #this is our password.

read -sp "Please enter the password:" PASSWORD

echo -e "\n"

if [ "$PASSWORD" == "$VALID_PASSWORD" ]; then
	echo "You have access!"
else
	echo "ACCESS DENIED!"
fi
