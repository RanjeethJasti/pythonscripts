#!/bin/bash

#Simple program to take mysql database backup

mkdir -p /home/backup

#read -p "Enter the name of db for which you need to take back: " dbname

dbname=$1

mysqldump -u root -p'admin@123' $dbname > /home/backup/$dbname.sql >> /dev/null 2>$1

if [ $? != 0 ] ; then

   #Some logic to be executed if script fails
   #Logic for sending out email
   echo "Script Failed!!"

else

  echo "Script executed succesfully!!"
   
fi
