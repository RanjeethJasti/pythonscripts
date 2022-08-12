import boto3

client = boto3.client('ec2')

response = client.run_instances(
    ImageId='ami-090fa75af13c156b4',
    InstanceType='t2.micro',
    MaxCount=1,
    MinCount=1,
    NetworkInterfaces=[
        {
            'AssociatePublicIpAddress': True,
            'DeviceIndex': 0,
            'SubnetId': 'subnet-0b24383d565f1f9e1',
        	'Groups': [
                'sg-04417becf67b0a812',
            ],
        },
    ],
)

print(response)
