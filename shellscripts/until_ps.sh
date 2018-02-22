#!/bin/bash

Stop="N"
until [ $Stop = "Y" ]; do
  w
  read -p "Want to stop? (Y/N)" reply
  Stop=`echo $reply | tr [:lower:] [:upper:]`
done
echo "done"

