#!/bin/bash

#Implement if condition

read -p "Enter your age: " age

if  [ $age -le 18 ]

then
   echo "You are a minor!!"
else
   echo "You are an adult!!"
fi


