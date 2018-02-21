#!/bin/bash

#Implement if elif

read -p "Enter a number: " num

if [ $num -le 10 ] ; then
   echo "$num is less than or equal to 10"
elif [ $num -lt 25 ] ; then
   echo "$num is greater 10 but less than 25"
elif [ $num -lt 100 ] ; then
   echo "$num is greater 25 but less than 100"
elif [ "$num" -eq "100" ] ; then
   echo "$num is 100"
else
   echo "$num is greater than 100"
fi
