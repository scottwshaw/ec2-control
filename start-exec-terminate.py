#/usr/bin/python
 
import boto3
import pprint as pp
import fabric
from fabric.api import env, run
from time import sleep

def hostname():
    print('hostname is ' + run('hostname'))

def mytask():
    hostname()

def execute_remote_task(host):
    env.hosts = ['ec2-user@' + host]
    env.key_filename = 'AWSKey02.pem'
    fabric.tasks.execute(mytask)

def launch_instance(ami):
    tag_spec = [{'ResourceType':'instance','Tags':[{'Key':'myinstance', 'Value':''}]}]
    response = ec2.run_instances(ImageId=ami,
                                 InstanceType='t2.micro',
                                 KeyName='AWSKey02',
                                 SecurityGroups=['launch-wizard-2'],
                                 TagSpecifications=tag_spec,
                                 MinCount=1,
                                 MaxCount=1)
    iid = response[u'Instances'][0][u'InstanceId']
    print('instance_id is ' + iid)
    return iid


def host_dns(iid):
    res = ec2.describe_instances(InstanceIds=[instance_id])
    return res[u'Reservations'][0][u'Instances'][0][u'PublicDnsName']

def wait_til_running(iid):
    print('waiting for running...')
    running_waiter = ec2.get_waiter(u'instance_running')
    running_waiter.wait(InstanceIds=[instance_id])
    print('instance is running')
    dns = host_dns(instance_id)
    print('host dns is...' + dns)
    return dns

def wait_til_ready(iid):
    print('waiting for ok...')
    ok_waiter = ec2.get_waiter(u'instance_status_ok')
    ok_waiter.wait(InstanceIds=[instance_id])
    print('instance is OK')

def terminate_instance(iid):
    print('terminating ' + iid)
    ec2.terminate_instances(InstanceIds=[iid])


ec2 = boto3.client('ec2')
ubuntu_ami = 'ami-e94e5e8a'
linux_ami = 'ami-ff4ea59d'
tensorflow_ami = 'ami-52332031'
deep_learning_with_source_code_ami = 'ami-bf866bdd'

instance_id = launch_instance(tensorflow_ami)
public_dns = wait_til_running(instance_id)
wait_til_ready(instance_id)
execute_remote_task(public_dns)
terminate_instance(instance_id)
