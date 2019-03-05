#!/usr/bin/python

import boto

ec2conn = boto.connect_ec2(aws_access_key_id="AKIAIRGA5N7F5T7EP2JQ", aws_secret_access_key="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")


ami_id = raw_input("Enter AMI ID:")
num_insts = raw_input("\nEnter number of instances that you need to launch:")
inst_type = raw_input("\n Eneter instance type: ")

try:
	ec2conn.run_instances(ami_id, min_count=num_insts, key_name="devopstraining", security_groups_ids=["sg-3597e346", "sg-8f9eeafc"], instance_type=in
	, subnet_id="subnet-8a132fa6")
	print "Machine got created successfully"
except Exception as e:
	print e
	print "Failure!!"