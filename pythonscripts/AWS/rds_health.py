import boto3
from datetime import datetime, timedelta

def get_db_identifiers(region):
    """Return a list of all db identifiers"""

    client = boto3.client('rds', region)
    db_instances = client.describe_db_instances()
    db_identifier_list = []
    for inst in db_instances['DBInstances']:
        db_identifier_list.append(inst['DBInstanceIdentifier'])
    return db_identifier_list

def rds_fetch_metrics(dbidentifier, metric):
    """Find average avalue of a cloudwatch matric"""

    cloudwatch = boto3.client('cloudwatch')
    response = cloudwatch.get_metric_data(
                    MetricDataQueries=[
                    {
                    'Id': "dbmetric",
                    'MetricStat': {
                        'Metric': {
                        'Namespace': 'AWS/RDS',
                        'MetricName': metric,
                        'Dimensions': [
                        {
                            'Name': 'DBInstanceIdentifier',
                            'Value': dbidentifier
                        },
                    ]
                    },
                'Period': 300,
                'Stat': 'Average',
                }
            }
        ],
        StartTime=datetime.now() - timedelta(minutes=30),
        EndTime=datetime.now()
        )
    return response['MetricDataResults'][0]['Values']

def rds_health(dbidentifier):
    """Do a basic health check of RDS
    based on cloud watch matrics and return dict"""

    gigabyte = 1.0/1024
    dbconn_list = rds_fetch_metrics(dbidentifier, 'DatabaseConnections')
    cpuaverage_list = rds_fetch_metrics(dbidentifier, 'CPUUtilization')
    free_diskspace_list = rds_fetch_metrics(dbidentifier, 'FreeStorageSpace')
    free_memory_list = rds_fetch_metrics(dbidentifier, 'FreeableMemory')
    dbconn_list.sort()
    cpuaverage_list.sort()
    free_diskspace_list.sort()
    free_memory_list.sort()
    free_space_gb = free_diskspace_list[0] * gigabyte * gigabyte * gigabyte
    free_memory_gb = free_memory_list[0] * gigabyte * gigabyte * gigabyte
    print "DB metric details of %s" %dbidentifier
    print "-------------------------------- \n \n"
    print "Average number of connections: %s" %str(dbconn_list[0])
    print "Average CPU usage percentage: %s" %(str("{0:.2f}".format(round(cpuaverage_list[0],2))))
    print "Free disk space: %s" %(str("{0:.2f}".format(round(free_space_gb,2))) + "GB")
    print "Free memory: %s" %(str("{0:.2f}".format(round(free_memory_gb, 2))) + "GB")
    print "\n \n"

if __name__ == '__main__':

    list_db_identifiers = get_db_identifiers('us-east-1')
    for dbidentifier in list_db_identifiers:
        rds_health(dbidentifier)