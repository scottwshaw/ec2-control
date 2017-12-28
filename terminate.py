#/usr/bin/python
 
import boto3
import pprint as pp

ec2 = boto3.client('ec2')
reservations = ec2.describe_instances(Filters=[
    {
        'Name':'tag-key',
        'Values':['myinstance']
    },
    {
        'Name': 'instance-state-name',
        'Values': ['pending','running']
    }

])
# pp.pprint(reservations)
iids = [res[u'Instances'][0][u'InstanceId'] for res in reservations[u'Reservations']]
print('terminating...')
print(iids)
if iids: ec2.terminate_instances(InstanceIds=iids)
