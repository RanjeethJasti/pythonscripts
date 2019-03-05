import boto3
import argparse
import sys
import logging
import os
import paramiko
import time
from configparser import ConfigParser
from datetime import datetime, timedelta
import urllib3
import warnings
warnings.filterwarnings("ignore")
urllib3.disable_warnings()
logname = "deployment.log"

logging.basicConfig(filename=logname,
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            level=logging.INFO)

logging.getLogger('boto3').propagate = False
logging.getLogger('boto3').setLevel(logging.INFO)
logging.getLogger('botocore').setLevel(logging.CRITICAL)
logging.getLogger('urllib3').setLevel(logging.CRITICAL)
logging.getLogger('cryptography.hazmat').setLevel(logging.CRITICAL)
logging.getLogger().addHandler(logging.StreamHandler())

def main():
	parser = argparse.ArgumentParser()
	subparsers = parser.add_subparsers()

	deploy_parser = subparsers.add_parser('deploy-app', help='Find AMIs older than age')
	deploy_parser.set_defaults(func=deploy_app)
	deploy_parser.add_argument('--app-name', choices=['myfin','myapp','testapp'], help='Enter the name of app that you need to deploy')
	deploy_parser.add_argument('--version', help='Version of app that you want to deploy')
	deploy_parser.add_argument('--region', help='AWS region on which you need to deploy this application')
	args = parser.parse_args()
	args.func(args)

def ec2_connection(region):
	"""return an EC2 connection object"""

	ec2_client = boto3.client('ec2', region_name=region)
	return ec2_client

def elb_connection(region):
	"""return an EC2 connection object"""

	elb_client = boto3.client('elb', region_name=region)
	return elb_client

def ec2_resource(region):
	"""Return an EC2 resource object"""

	ec2_resource = boto3.resource('ec2', region_name=region)
	return ec2_resource


def parse_config(app):
	"""Parse the config file for app
	that need to be deployed and get
	relevant values"""

	parser = ConfigParser()
	config_file = ("envConf.cfg")
	parser.read(config_file)
	return parser

def find_instances(elb, region):
	"""Find all instances that are configured 
	under an ELB"""
	
	elb_client = elb_connection(region)
	response = elb_client.describe_load_balancers(
      LoadBalancerNames =  [elb]
  	)

  	instance_ids = []
  	for instance in response['LoadBalancerDescriptions'][0]['Instances']:
  		instance_ids.append(instance['InstanceId'])

  	return instance_ids

def remove_inst_from_elb(elb, instance_id, region):

	"""Remove instances from Load balancer"""

	try:
		elb_client = elb_connection(region)
		logging.info("Deregistering instance: %s from ELB: %s" % (instance_id, elb))
		response = elb_client.deregister_instances_from_load_balancer(
    				LoadBalancerName= elb,
    				Instances=[
        			{
            		'InstanceId': instance_id
       				}
    				]
				)
		logging.info("Successfully deregistered instance: %s from ELB: %s" % (instance_id, elb))
	except Exception as e:
		logging.error("Error while deregistering instance: %s from ELB: %s" % (instance_id, elb))

def add_instance_to_elb(elb, instance_id, region):

	"""Add an ec2 instance to ELB"""
	
	try:
		logging.info("Registering instance: %s to ELB: %s" % (instance_id, elb))
		elb_client = elb_connection(region)
		response = elb_client.register_instances_with_load_balancer(
    				LoadBalancerName=elb,
    				Instances=[
        				{
            			'InstanceId': instance_id
        				},
    				]
				)
	except Exception as e:
		logging.error("Failed to register instance: %s to ELB: %s" % (instance_id, elb))
		logging.error(e)

	logging.info("Waiting for instance %s to be 'Inservice'" % (instance_id))

	for i in range(10):
		time.sleep(10)
		response = elb_client.describe_instance_health(
						LoadBalancerName=elb,
						Instances=[
							{
							'InstanceId': instance_id
							},
						]
					)
		if response['InstanceStates'][0]['State'] == "InService":
			logging.info("Instance %s is InService" % (instance_id))
			return
		else:
			continue
	logging.error("Failed to bring instance %s InService" % (instance_id))

def find_instance_ip(instance, region):
	"""Find IP, and credentials of EC2 
	instance"""

	resource = ec2_resource(region)
	inst_obj = resource.Instance(instance)
	private_ip = inst_obj.private_ip_address
	return private_ip

def run_deployment_command(hostname, username, keyfile, command):
	"""Run chef command for deployment on ec2 instance"""

	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(hostname, username=username, key_filename=keyfile)
	chan = ssh.get_transport().open_session()
	chan.exec_command(command)
	exitstatus = chan.recv_exit_status()
	ssh.close()
	return exitstatus

def deploy_app(args):
	"""Function to deploy the application"""

	logging.info("Starting deployment on APP: %s. Deploying version: %s" % (args.app_name, args.version))
	app_config = parse_config(args.app_name)
	elb = app_config.get(args.app_name, 'elb')
	username = app_config.get(args.app_name, 'username')
	keyname = app_config.get(args.app_name, 'key')
	command = 'sudo chef-client'
	instance_ids = find_instances(elb, args.region)
	if instance_ids:
		for instance in instance_ids:
			remove_inst_from_elb(elb, instance, args.region)
			time.sleep(5)
			private_ip = find_instance_ip(instance, args.region)
			logging.info("Running checf client on %s. Deploying version: %s" % (private_ip, args.version))
			exit_status = run_deployment_command(private_ip, username, keyname, command)
			if exit_status != 0:
				logging.error("Deployment failed on instance: %s. Please investigate. Exiting"  % (instance))
				sys.exit(1)
			add_instance_to_elb(elb, instance, args.region)
		logging.info("Deployment of Application: %s version %s is completed successfully!!" % (args.app_name, args.version))
	else:
		logging.info("No instances found under the LB: %s. Exiting" % (elb))
		sys.exit(0)

if __name__ == '__main__':
	main()