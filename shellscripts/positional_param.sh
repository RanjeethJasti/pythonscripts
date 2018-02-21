#!/bin/bash

#Understanding positional parameters

echo $0
echo "Display positional parameters:"

echo "First positional parameter is: $1"
echo "Second positional parameter is: $2"
echo "Third positional parameter is: $3"
echo "Fourth positional parameter is: $4"
echo "Fifth positional parameter is: $5"


echo "Number of positional parameters is: $#"
echo "All positional parameters as single string: $*"
echo "All positional parameters as seperate strings: $@"
echo "Process ID of current process: $$"

for i in $*
do
echo $i
done

for i in $@
do
echo $@
done


