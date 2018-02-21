#!/usr/bin/python

fin = open("newfile.txt")
fout = open("tempfile.txt", "a")

for line in fin.readlines():
   if  "hello world" in line:
	print line
	fout.write("welcome devops training\n")
   else:
	fout.write(line)
fin.close()
fout.close()
