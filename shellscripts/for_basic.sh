#!/bin/bash

cd /home/vagrant/script_backup

for filename in `ls` 
do
   rm $filename
done
