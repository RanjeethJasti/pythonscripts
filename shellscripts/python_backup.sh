#!/bin/bash

mkdir -p /backup/pythonscripts
cd /data/pythonscripts
for i in `ls | grep ".py"`
 do
 cp $i /backup/pythonscripts
 done
