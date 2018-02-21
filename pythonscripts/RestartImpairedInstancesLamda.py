import json
from boto3 import client



def stop_instances(impaired_instances):
    """Stop all impaired instances"""
    print  "Stopping " + str(impaired_instances)

    stop_response = ec2_client.stop_instances(
        InstanceIds=impaired_instances,
        Force=True
    )

    print stop_response

    stop_waiter = ec2_client.get_waiter('instance_stopped')

    stop_waiter.wait(
        InstanceIds=impaired_instances
    )

def start_instances(impaired_instances):
    """Start all impaired instances"""
    print  "Starting " + str(impaired_instances)

    start_response = ec2_client.start_instances(
        InstanceIds=impaired_instances
    )

    print start_response

    start_waiter = ec2_client.get_waiter('instance_running')

    start_waiter.wait(
        InstanceIds=impaired_instances
    )

def lambda_handler(event, context):
    """Main function"""

    if context:
        myregion = context.invoked_function_arn.split(':')[3]
    else:
        myregion = 'us-west-2'
    
    filter1 = [
        {
            'Name': 'instance-status.status',
            'Values': ['ok']}
    ]

    impaired_instances = []
    
    
    ec2_client = client("ec2", myregion)
    
    #First Filter
    f1 = ec2_client.describe_instance_status(DryRun=False, Filters=filter1)
    print "First Filter results is", json.dumps(f1, indent=4, sort_keys=True, default=str)

    for i  in f1['InstanceStatuses']:
        impaired_instances.append(i['InstanceId'])
    print "Impaired instances: ", impaired_instances

    if impaired_instances:
        print "Stopping and Starting the Instances"
        stop_instances(impaired_instances)
        start_instances(impaired_instances)


    print "Final Status of Impaired Instances", ec2_client.describe_instance_status(DryRun=False, \
            InstanceIds=impaired_instances)
    return 0
