#!/bin/bash
echo "Enter a filename: "
read filename
if [ -f "$filename" ]
 then
   echo "$filename is a file"
 exit 1
 elif [ -d "$filename" ]
   then
   echo "$filename is a directory"
 else 
   echo "$filename does not exist"
 fi
