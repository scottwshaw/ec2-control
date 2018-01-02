#/usr/bin/python
 
import boto3
import pprint as pp
import fabric
from fabric.api import env, run, settings
from time import sleep

UBUNTU_AMI = 'ami-e94e5e8a'
LINUX_AMI = 'ami-ff4ea59d'
TENSORFLOW_AMI = 'ami-52332031'
DEEP_LEARNING_WITH_SOURCE_CODE_AMI = 'ami-bf866bdd'

def launch_instance(ec2, ami):
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


def host_dns(ec2, iid):
    res = ec2.describe_instances(InstanceIds=[instance_id])
    return res[u'Reservations'][0][u'Instances'][0][u'PublicDnsName']

def wait_til_running(ec2, iid):
    print('waiting for running...')
    running_waiter = ec2.get_waiter(u'instance_running')
    running_waiter.wait(InstanceIds=[instance_id])
    print('instance is running')
    dns = host_dns(ec2, instance_id)
    print('host dns is...' + dns)
    return dns

def wait_til_ready(ec2, iid):
    print('waiting for ok...')
    ok_waiter = ec2.get_waiter(u'instance_status_ok')
    ok_waiter.wait(InstanceIds=[instance_id])
    print('instance is OK')

def terminate_instance(ec2, iid):
    print('terminating ' + iid)
    ec2.terminate_instances(InstanceIds=[iid])

def copy_script_to_remote():
    print('copying to remote...')
    fabric.operations.put('simple-graph.py','script.py')
    print('copied')

class FabricException(Exception):
    pass

def execute_script(ec2):
    print('executing...')
    with settings(abort_exception = FabricException):
        try:
            run('python script.py > script-output.txt 2>&1')
        except FabricException as err:
            print("remote execution error: {0}".format(err))

def print_output(fname):
    print('Output fromn script was...')
    with open(fname, 'r') as fin:
        print fin.read()

def copy_output_to_local():
    fname = 'script-output.txt'
    pname = env.hosts[0] + '/' + fname
    print('retrieving output to ' + pname)
    fabric.operations.get(fname)
    print_output(pname)
    

def exec_script_remotely(ec2):
    fabric.tasks.execute(copy_script_to_remote)
    print('executing on ')
    print(env.hosts)
    fabric.tasks.execute(execute_script, ec2, hosts=env.hosts)
    fabric.tasks.execute(copy_output_to_local)

env.key_filename='AWSKey02.pem'
ec2_client = boto3.client('ec2')
instance_id = launch_instance(ec2_client, TENSORFLOW_AMI)
public_dns = wait_til_running(ec2_client, instance_id)
# instance_id = 'i-094c8ea7994e7f856'
# public_dns = 'ec2-52-63-249-43.ap-southeast-2.compute.amazonaws.com'
env.hosts=['ec2-user@'+public_dns]
wait_til_ready(ec2_client, instance_id)
exec_script_remotely(ec2_client)
terminate_instance(ec2_client, instance_id)
