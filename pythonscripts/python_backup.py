#!/usr/bin/python

import os, shutil

# This is a simple script to backup python files from "/data/pythonscripts/" to "/backuppythonscripts/"

#Create a backup directory

src_dir = '/data/pythonscripts/'
dest_dir = '/backup/pythonscripts/'

os.makedirs(dest_dir)
os.chdir(src_dir)

list_item = os.listdir(src_dir)
for item in list_item:
	if ".py" in item:
		shutil.copy(item, dest_dir)
