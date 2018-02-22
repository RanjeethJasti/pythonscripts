#!/bin/bash

Cont="Y"
while [ $Cont = "Y" ]; do
  w
  read -p "want to continue? (Y/N)" reply
  Cont=`echo $reply | tr [:lower:] [:upper:]`
done
echo "done"

