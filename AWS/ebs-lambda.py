import boto3

def lambda_handler(event, context):
    ec2 = boto3.resource('ec2',region_name='us-east-1')
    
    for vol in ec2.volumes.all():
        
        if  vol.state=='available':
            if vol.tags is None:
                vid=vol.id
                vol.delete()
                print ('Deleted ' +vid)
                continue
            tag_keys = {}
            for tag in vol.tags:
                tag_keys[tag['Key']] = tag['Value']
                
            if 'deletePolicy' in tag_keys.keys():
                    if tag_keys['deletePolicy'] != 'DND':
                        vid=vol.id
                        vol.delete()
                        print ('Deleted ' +vid)
            else:
                vid=vol.id
                vol.delete()
                print ('Deleted ' +vid)